"""Tests for DeepRAGPipeline construction and from_config factory."""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock

from src.ai.rag.deep_rag_pipeline import DeepRAGPipeline


class TestDeepRAGPipeline(unittest.TestCase):
    """Unit tests for DeepRAGPipeline construction."""

    def setUp(self) -> None:
        self.llm = MagicMock()
        self.retriever = MagicMock()

    def test_construction(self) -> None:
        pipeline = DeepRAGPipeline(llm=self.llm, retriever=self.retriever)
        assert pipeline.llm is self.llm
        assert pipeline.retriever is self.retriever

    def test_from_config(self) -> None:
        config: dict[str, object] = {"llm": self.llm, "retriever": self.retriever}
        pipeline = DeepRAGPipeline.from_config(config)
        assert pipeline.llm is self.llm
        assert pipeline.retriever is self.retriever

    def test_from_config_missing_llm_raises(self) -> None:
        with self.assertRaises(ValueError, msg="llm is required"):
            DeepRAGPipeline.from_config({"retriever": self.retriever})

    def test_from_config_missing_retriever_raises(self) -> None:
        with self.assertRaises(ValueError, msg="retriever is required"):
            DeepRAGPipeline.from_config({"llm": self.llm})


if __name__ == "__main__":
    unittest.main()