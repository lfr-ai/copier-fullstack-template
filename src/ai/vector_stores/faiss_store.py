"""FAISS vector store adapter."""

from __future__ import annotations

from typing import Any, final

import json
import structlog
from pathlib import Path

from ai.config import DEFAULT_SEARCH_TOP_K
from core.interfaces.vector_store import VectorSearchResult, VectorStoreGateway

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class _NumpyIndexFlatL2:
    """Minimal FAISS IndexFlatL2-compatible fallback using numpy."""

    __slots__ = ("_dimension", "_vectors")

    def __init__(self, dimension: int) -> None:
        self._dimension = dimension
        self._vectors: list[list[float]] = []

    @property
    def ntotal(self) -> int:
        return len(self._vectors)

    def add(self, vectors: Any) -> None:
        for vec in vectors.tolist():
            self._vectors.append(list(vec))

    def search(self, query: Any, top_k: int) -> tuple[Any, Any]:
        import numpy as np

        q = np.asarray(query, dtype=np.float32)[0]
        if not self._vectors:
            return np.array([[]], dtype=np.float32), np.array([[]], dtype=np.int64)

        mat = np.asarray(self._vectors, dtype=np.float32)
        dists = np.sum((mat - q) ** 2, axis=1)
        order = np.argsort(dists)[:top_k]
        return np.array([dists[order]], dtype=np.float32), np.array([order], dtype=np.int64)

    def reconstruct(self, idx: int) -> Any:
        import numpy as np

        return np.asarray(self._vectors[idx], dtype=np.float32)


@final
class FaissVectorStore(VectorStoreGateway):
    """FAISS-backed vector store with metadata and persistence support."""

    __slots__ = ("_dimension", "_id_to_idx", "_idx_to_id", "_index", "_metadata_store", "_faiss")

    def __init__(self, *, dimension: int, persist_dir: str | None = None) -> None:
        try:
            import faiss  # type: ignore[import-untyped]
            self._faiss = faiss
            self._index = faiss.IndexFlatL2(dimension)
        except ImportError:
            self._faiss = None
            self._index = _NumpyIndexFlatL2(dimension)
            logger.warning("faiss-cpu not installed; using numpy fallback index")

        self._dimension = dimension
        self._id_to_idx: dict[str, int] = {}
        self._idx_to_id: dict[int, str] = {}
        self._metadata_store: dict[str, dict[str, object]] = {}

        if persist_dir:
            self._load_if_exists(persist_dir)

    @classmethod
    def from_config(cls, config: dict[str, object]) -> FaissVectorStore:
        """Create a FaissVectorStore instance from a configuration dictionary.

        Expected config structure::

            {
                "dimension": 1536,
                "persist_dir": "/path/to/faiss/index",  # optional
            }

        Args:
            config (dict[str, object]): Configuration dictionary.

        Returns:
            FaissVectorStore: Configured vector store instance.
        """
        dimension = int(config["dimension"])
        persist_dir = config.get("persist_dir")

        return cls(
            dimension=dimension,
            persist_dir=str(persist_dir) if persist_dir is not None else None,
        )

    async def add_vectors(
        self,
        *,
        vectors: list[list[float]],
        ids: list[str],
        metadata: list[dict[str, object]] | None = None,
    ) -> None:
        import numpy as np

        if len(vectors) != len(ids):
            msg = "vectors and ids must have the same length"
            raise ValueError(msg)

        arr = np.array(vectors, dtype=np.float32)
        start_idx = self._index.ntotal
        self._index.add(arr)

        for i, vid in enumerate(ids):
            idx = start_idx + i
            self._id_to_idx[vid] = idx
            self._idx_to_id[idx] = vid
            if metadata and i < len(metadata):
                self._metadata_store[vid] = metadata[i]

        logger.info("Added %d vectors to FAISS index", len(ids))

    async def search(
        self,
        *,
        query_vector: list[float],
        top_k: int = DEFAULT_SEARCH_TOP_K,
        filters: dict[str, object] | None = None,
    ) -> list[VectorSearchResult]:
        import numpy as np

        if self._index.ntotal == 0:
            return []

        query = np.array([query_vector], dtype=np.float32)
        distances, indices = self._index.search(query, min(top_k, self._index.ntotal))

        results: list[VectorSearchResult] = []
        for dist, idx in zip(distances[0], indices[0], strict=True):
            if idx == -1:
                continue
            vid = self._idx_to_id.get(int(idx))
            if vid is None:
                continue
            if filters and not self._matches_filters(vid, filters):
                continue
            results.append(
                VectorSearchResult(
                    id=vid,
                    score=float(dist),
                    metadata=self._metadata_store.get(vid),
                )
            )
        return results

    async def delete_vectors(self, ids: list[str]) -> None:
        import numpy as np

        ids_to_delete = set(ids)
        keep_ids: list[str] = []
        keep_vectors: list[list[float]] = []

        for vid, idx in self._id_to_idx.items():
            if vid in ids_to_delete:
                self._metadata_store.pop(vid, None)
                continue
            vec = self._index.reconstruct(int(idx))
            keep_ids.append(vid)
            keep_vectors.append(vec.tolist())

        removed = len(self._id_to_idx) - len(keep_ids)

        # Rebuild the index from scratch with remaining vectors.
        if self._faiss is not None:
            self._index = self._faiss.IndexFlatL2(self._dimension)
        else:
            self._index = _NumpyIndexFlatL2(self._dimension)
        self._id_to_idx.clear()
        self._idx_to_id.clear()

        if keep_vectors:
            arr = np.array(keep_vectors, dtype=np.float32)
            self._index.add(arr)
            for i, vid in enumerate(keep_ids):
                self._id_to_idx[vid] = i
                self._idx_to_id[i] = vid

        logger.info("Deleted %d vectors and rebuilt FAISS index (%d remaining)", removed, len(keep_ids))

    async def count(self) -> int:
        return len(self._id_to_idx)

    def save(self, directory: str) -> None:
        """Persist the FAISS index and metadata to disk.

        Args:
            directory (str): Target directory (created if missing).
        """
        if self._faiss is None:
            logger.warning("Skipping save because faiss-cpu is not installed")
            return

        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        self._faiss.write_index(self._index, str(path / "index.faiss"))

        meta = {
            "id_to_idx": self._id_to_idx,
            "idx_to_id": {str(k): v for k, v in self._idx_to_id.items()},
            "metadata": self._metadata_store,
        }
        (path / "metadata.json").write_text(json.dumps(meta), encoding="utf-8")
        logger.info("FAISS index saved to %s", directory)

    def _load_if_exists(self, directory: str) -> None:
        if self._faiss is None:
            return

        path = Path(directory)
        index_path = path / "index.faiss"
        meta_path = path / "metadata.json"

        if index_path.exists() and meta_path.exists():
            self._index = self._faiss.read_index(str(index_path))
            raw = json.loads(meta_path.read_text(encoding="utf-8"))
            self._id_to_idx = raw["id_to_idx"]
            self._idx_to_id = {int(k): v for k, v in raw["idx_to_id"].items()}
            self._metadata_store = raw.get("metadata", {})
            logger.info("FAISS index loaded from %s (%d vectors)", directory, self._index.ntotal)

    def _matches_filters(self, vid: str, filters: dict[str, object]) -> bool:
        meta = self._metadata_store.get(vid, {})
        return all(meta.get(k) == v for k, v in filters.items())
