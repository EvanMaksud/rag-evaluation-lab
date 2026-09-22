# RAG Evaluation Lab

Local-first tooling for testing retrieval-augmented generation pipelines before an LLM is added.

The project focuses on a practical engineering problem: many RAG demos look good because the retrieval layer is never measured. This lab turns a folder of documents and a set of answerable questions into a repeatable retrieval benchmark with clear metrics, failure cases, and a Markdown or JSON report.

## What It Does

- Loads Markdown and text documents from a local corpus folder.
- Splits documents into configurable overlapping chunks.
- Builds a dependency-light TF-IDF retriever as a strong, inspectable baseline.
- Evaluates retrieval with `hit_rate@k`, `recall@k`, `precision@k`, `MRR@k`, and answer-term coverage.
- Writes readable reports with the top retrieved chunks for every question.
- Includes a reproducible public-corpus downloader using Wikipedia's public API.
- Runs fully offline after the corpus is downloaded.

## Why This Project Exists

RAG systems fail quietly when the retriever returns plausible but wrong context. A useful AI engineer should be able to measure that failure, not just wrap a vector database around documents and hope for the best.

This repo is deliberately built around evaluation:

- retrieval is separated from generation,
- every benchmark question has known relevant documents,
- metrics are deterministic,
- failure cases are visible in the report,
- experiments can be rerun with different chunk sizes and overlaps.

## Quick Start

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e . pytest
```

Run the included fixture benchmark:

```powershell
rag-eval evaluate examples\mini_corpus examples\mini_questions.jsonl --output reports\mini_report.md
```

Download a real public corpus and evaluate it:

```powershell
python scripts\download_public_corpus.py --output data\wikipedia_corpus
rag-eval evaluate data\wikipedia_corpus examples\wikipedia_questions.jsonl --output reports\wikipedia_report.md --k 5
```

The downloaded Wikipedia corpus is intentionally not committed. See [SOURCES.md](SOURCES.md) for source and license notes.

## Question Format

Each JSONL row contains a question, one or more relevant document IDs, and optional answer terms that should appear somewhere in the retrieved context.

```json
{"id":"q1","question":"What does retrieval evaluation measure before generation?","relevant_doc_ids":["rag_basics"],"answer_terms":["retrieval","generation"]}
```

Document IDs are derived from file names. For example, `rag_basics.md` becomes `rag_basics`.

## Example Metrics

```text
Questions: 8
Hit rate@5: 0.875
Recall@5: 0.812
Precision@5: 0.225
MRR@5: 0.646
Answer-term coverage: 0.781
```

## Project Structure

```text
rag_eval_lab/
  chunking.py       # deterministic overlapping chunker
  corpus.py         # document loading and normalization
  evaluation.py     # retrieval metrics and per-question outcomes
  retrievers.py     # TF-IDF baseline retriever
  report.py         # Markdown and JSON report rendering
  cli.py            # command-line interface
scripts/
  download_public_corpus.py
tests/
  test_*.py
```

## Notes

This is not presented as a production RAG platform. It is a focused evaluation lab that can be extended with embeddings, FAISS, Pinecone, rerankers, or LLM-as-judge evaluation after the retrieval baseline is understood.
