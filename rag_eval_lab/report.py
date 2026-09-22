from __future__ import annotations

import json

from .evaluation import EvaluationReport


def render_markdown(report: EvaluationReport) -> str:
    lines = [
        "# RAG Retrieval Evaluation Report",
        "",
        "## Summary",
        "",
        f"- Questions: **{report.question_count}**",
        f"- Hit rate@{report.k}: **{report.hit_rate:.3f}**",
        f"- Recall@{report.k}: **{report.recall_at_k:.3f}**",
        f"- Precision@{report.k}: **{report.precision_at_k:.3f}**",
        f"- MRR@{report.k}: **{report.mrr_at_k:.3f}**",
        f"- Answer-term coverage: **{report.answer_term_coverage:.3f}**",
        "",
        "## Per-Question Results",
        "",
    ]

    for result in report.question_results:
        lines.extend(
            [
                f"### {result.question.id}",
                "",
                f"Question: {result.question.question}",
                "",
                f"- Hit: **{result.hit}**",
                f"- Recall: **{result.recall:.3f}**",
                f"- Precision: **{result.precision:.3f}**",
                f"- Reciprocal rank: **{result.reciprocal_rank:.3f}**",
                f"- Answer-term coverage: **{result.answer_term_coverage:.3f}**",
                "",
                "| Rank | Score | Document | Chunk |",
                "| ---: | ---: | --- | --- |",
            ]
        )
        for item in result.results:
            preview = item.chunk.text[:140].replace("|", "\\|")
            lines.append(
                f"| {item.rank} | {item.score:.4f} | `{item.chunk.doc_id}` | {preview}... |"
            )
        lines.append("")

    return "\n".join(lines)


def render_json(report: EvaluationReport) -> str:
    payload = {
        "k": report.k,
        "question_count": report.question_count,
        "metrics": {
            "hit_rate": report.hit_rate,
            "recall_at_k": report.recall_at_k,
            "precision_at_k": report.precision_at_k,
            "mrr_at_k": report.mrr_at_k,
            "answer_term_coverage": report.answer_term_coverage,
        },
        "questions": [
            {
                "id": result.question.id,
                "question": result.question.question,
                "relevant_doc_ids": sorted(result.question.relevant_doc_ids),
                "hit": result.hit,
                "recall": result.recall,
                "precision": result.precision,
                "reciprocal_rank": result.reciprocal_rank,
                "answer_term_coverage": result.answer_term_coverage,
                "results": [
                    {
                        "rank": item.rank,
                        "score": item.score,
                        "doc_id": item.chunk.doc_id,
                        "chunk_id": item.chunk.chunk_id,
                        "title": item.chunk.title,
                    }
                    for item in result.results
                ],
            }
            for result in report.question_results
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True)

