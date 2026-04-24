"""Provide cross-encoder reranking adapter implementation."""

from __future__ import annotations

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

from ..interfaces.reranker import RerankerGateway, RankedResult


class CrossEncoderReranker(RerankerGateway):
    """Cross-Encoder based reranker implementation."""

    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    async def rerank(
        self,
        *,
        query: str,
        results: list[dict[str, object]],
        top_k: int = 5,
    ) -> list[RankedResult]:
        """Rerank search results using the Cross-Encoder model."""
        rerank_scores = []
        for result in results:
            inputs = self.tokenizer(
                [query] * len(results),
                [res['content'] for res in results],
                padding=True,
                truncation=True,
                return_tensors="pt",
            )
            with torch.no_grad():
                outputs = self.model(**inputs).logits
                scores = torch.softmax(outputs, dim=-1)[:, 1].tolist()
                rerank_scores.append(scores)

        ranked_results = sorted(
            [RankedResult(
                id=res.get('id', ''),
                content=res['content'],
                original_score=res['score'],
                rerank_score=rerank_scores[idx],
                metadata=res.get('metadata', {}),
            )
                for idx, res in enumerate(results)
            ],
            key=lambda x: x.rerank_score, reverse=True
        )
        return ranked_results[0:top_k]
