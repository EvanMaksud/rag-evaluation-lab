from __future__ import annotations

import argparse
from pathlib import Path

from .chunking import chunk_documents
from .corpus import load_corpus
from .evaluation import evaluate_retriever, load_questions
from .report import render_json, render_markdown
from .retrievers import TfidfRetriever


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate retrieval quality for a RAG corpus.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Run a retrieval benchmark.")
    evaluate.add_argument("corpus", help="Folder containing Markdown or text documents.")
    evaluate.add_argument("questions", help="JSONL benchmark questions.")
    evaluate.add_argument("--k", type=int, default=5, help="Number of chunks to retrieve.")
    evaluate.add_argument("--chunk-size", type=int, default=180)
    evaluate.add_argument("--overlap", type=int, default=40)
    evaluate.add_argument("--format", choices=["markdown", "json"], default="markdown")
    evaluate.add_argument("--output", "-o", help="Write report to a file.")

    args = parser.parse_args(argv)
    if args.command == "evaluate":
        return run_evaluate(args)
    return 2


def run_evaluate(args: argparse.Namespace) -> int:
    documents = load_corpus(args.corpus)
    chunks = chunk_documents(documents, chunk_size=args.chunk_size, overlap=args.overlap)
    questions = load_questions(args.questions)
    report = evaluate_retriever(TfidfRetriever(chunks), questions, k=args.k)
    body = render_json(report) if args.format == "json" else render_markdown(report)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(body, encoding="utf-8")
    else:
        print(body)

    return 0

