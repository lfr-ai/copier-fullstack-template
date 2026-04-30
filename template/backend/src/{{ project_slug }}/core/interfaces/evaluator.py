"""Evaluator gateway -- abstract interface for LLM output evaluation.

Supports automated quality assessment of LLM outputs using
rubric-based scoring, LLM-as-judge patterns, and custom metrics.
Concrete adapters may use DeepEval, Ragas, LangSmith, or custom
evaluation pipelines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable, final


@dataclass(frozen=True, slots=True)
@final
class EvalResult:
    """Result from a single evaluation."""

    metric: str
    score: float
    passed: bool
    reason: str = ""
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
@final
class EvalSuite:
    """Aggregated results from an evaluation suite run."""

    results: list[EvalResult] = field(default_factory=list)
    overall_score: float = 0.0
    passed: bool = True

    @property
    def failed_metrics(self) -> list[str]:
        """Return names of metrics that did not pass."""
        return [r.metric for r in self.results if not r.passed]


@runtime_checkable
class EvaluatorGateway(Protocol):
    """Gateway for LLM output evaluators.

    Evaluators assess the quality of LLM-generated outputs
    against expected criteria (relevance, faithfulness,
    coherence, safety, etc.).
    """

    async def evaluate(
        self,
        *,
        question: str,
        answer: str,
        context: str = "",
        expected: str = "",
    ) -> EvalResult:
        """Evaluate a single LLM output.

        Args:
            question (str): The input question or prompt.
            answer (str): The LLM-generated answer to evaluate.
            context (str): Retrieved context used for generation (for RAG evals).
            expected (str): Expected/reference answer (for comparison evals).

        Returns:
            EvalResult: Evaluation result with score and reasoning.
        """
        ...

    async def evaluate_batch(
        self,
        *,
        samples: list[dict[str, str]],
    ) -> EvalSuite:
        """Run evaluation across multiple samples.

        Args:
            samples (list[dict[str, str]]): List of dicts with keys matching evaluate() params.

        Returns:
            EvalSuite: Aggregated evaluation suite results.
        """
        ...
