"""Tests for DeepRAGPipeline observability and lazy graph init."""

from __future__ import annotations

import logging
from unittest.mock import MagicMock

import pytest

from src.ai.rag.deep_rag_pipeline import DeepRAGPipeline

logger = logging.getLogger("test_observability")


@pytest.fixture()
def llm_mock() -> MagicMock:
    return MagicMock()


@pytest.fixture()
def retriever_mock() -> MagicMock:
    return MagicMock()


@pytest.fixture()
def pipeline(llm_mock: MagicMock, retriever_mock: MagicMock) -> DeepRAGPipeline:
    return DeepRAGPipeline(llm=llm_mock, retriever=retriever_mock)


def test_pipeline_creates_successfully(pipeline: DeepRAGPipeline) -> None:
    assert pipeline is not None
    assert pipeline.llm is not None
    assert pipeline.retriever is not None


def test_pipeline_logs_initialization(
    caplog: pytest.LogCaptureFixture,
    llm_mock: MagicMock,
    retriever_mock: MagicMock,
) -> None:
    caplog.set_level(logging.DEBUG)
    DeepRAGPipeline(llm=llm_mock, retriever=retriever_mock)
    assert "DeepRAGPipeline initialized" in caplog.text