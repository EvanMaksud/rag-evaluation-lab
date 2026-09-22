from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .retrievers import SearchResult, TfidfRetriever


@dataclass(frozen=True)
class Question:
    id: str
    question: str
    relevant_doc_ids: set[str]
    answer_terms: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class QuestionResult:
    question: Question
    results: list[SearchResult]
    hit: bool
    recall: float
    precision: float
    reciprocal_rank: float
    answer_term_coverage: float


@dataclass(frozen=True)
class EvaluationReport:
    k: int
    question_results: list[QuestionResult]

    @property
    def question_count(self) -> int:
        return len(self.question_results)

    @property
    def hit_rate(self) -> float:
        return mean(1.0 if result.hit else 0.0 for result in self.question_results)

    @property
    def recall_at_k(self) -> float:
        return mean(result.recall for result in self.question_results)

    @property
    def precision_at_k(self) -> float:
        return mean(result.precision for result in self.question_results)

    @property
    def mrr_at_k(self) -> float:
        return mean(result.reciprocal_rank for result in self.question_results)

    @property
    def answer_term_coverage(self) -> float:
        return mean(result.answer_term_coverage for result in self.question_results)


def load_questions(path: str | Path) -> list[Question]:
    questions: list[Question] = []
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        payload = json.loads(line)
        relevant = set(payload.get("relevant_doc_ids", []))
        if not relevant:
            raise ValueError(f"Question at line {line_number} has no relevant_doc_ids")
        questions.append(
            Question(
                id=str(payload["id"]),
                question=str(payload["question"]),
                relevant_doc_ids=relevant,
                answer_terms={str(term).lower() for term in payload.get("answer_terms", [])},
            )
        )
    if not questions:
        raise ValueError(f"No questions found in {path}")
    return questions


def evaluate_retriever(
    retriever: TfidfRetriever,
    questions: list[Question],
    k: int = 5,
) -> EvaluationReport:
    results: list[QuestionResult] = []
    for question in questions:
        retrieved = retriever.search(question.question, k=k)
        retrieved_doc_ids = [item.chunk.doc_id for item in retrieved]
        relevant_retrieved = [
            doc_id for doc_id in retrieved_doc_ids if doc_id in question.relevant_doc_ids
        ]
        reciprocal_rank = 0.0
        for item in retrieved:
            if item.chunk.doc_id in question.relevant_doc_ids:
                reciprocal_rank = 1.0 / item.rank
                break

        context = " ".join(item.chunk.text.lower() for item in retrieved)
        if question.answer_terms:
            covered_terms = [term for term in question.answer_terms if term in context]
            answer_coverage = len(covered_terms) / len(question.answer_terms)
        else:
            answer_coverage = 0.0

        results.append(
            QuestionResult(
                question=question,
                results=retrieved,
                hit=bool(relevant_retrieved),
                recall=len(set(relevant_retrieved)) / len(question.relevant_doc_ids),
                precision=len(relevant_retrieved) / len(retrieved) if retrieved else 0.0,
                reciprocal_rank=reciprocal_rank,
                answer_term_coverage=answer_coverage,
            )
        )
    return EvaluationReport(k=k, question_results=results)


def mean(values) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)

