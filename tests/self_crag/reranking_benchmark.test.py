from time import time

import pytest
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from {{ project_slug }}.core.adapters.cross_encoder_reranker import CrossEncoderReranker

@pytest.mark.performance
@pytest.mark.asyncio
async def test_cross_encoder_reranker_latency():
    reranker = CrossEncoderReranker("cross-encoder/msmarco-TinyBERT-L-6")

    query = "What are the best practices for deploying machine learning models?"
    results = [
        {"content": "Model serving best practices include scaling, updating, and monitoring deployed models.", "score": 0.8},
        {"content": "To deploy a machine learning model, consider using frameworks such as TorchServe and TensorFlow Serving.", "score": 0.7},
    ]

    start_time = time()
    ranked_results = await reranker.rerank(query=query, results=results)
    elapsed_time = time() - start_time

    assert elapsed_time < 0.2, "Reranking latency must be under 200 ms"
    assert ranked_results[0].rerank_score >= ranked_results[1].rerank_score, "Results must be properly ordered"
