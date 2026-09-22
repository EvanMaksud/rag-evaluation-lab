from pathlib import Path

from rag_eval_lab.chunking import chunk_documents
from rag_eval_lab.corpus import load_corpus
from rag_eval_lab.evaluation import evaluate_retriever, load_questions
from rag_eval_lab.retrievers import TfidfRetriever


def test_retrieval_evaluation_finds_relevant_document(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "rag_basics.md").write_text(
        "# RAG Basics\nRetrieval augmented generation uses retrieved context before generation.",
        encoding="utf-8",
    )
    (corpus / "serving.md").write_text(
        "# Serving\nModel APIs validate inputs and return predictable outputs.",
        encoding="utf-8",
    )
    questions = tmp_path / "questions.jsonl"
    questions.write_text(
        '{"id":"q1","question":"What uses retrieved context before generation?",'
        '"relevant_doc_ids":["rag_basics"],"answer_terms":["context","generation"]}\n',
        encoding="utf-8",
    )

    documents = load_corpus(corpus)
    chunks = chunk_documents(documents, chunk_size=30, overlap=5)
    report = evaluate_retriever(TfidfRetriever(chunks), load_questions(questions), k=2)

    assert report.question_count == 1
    assert report.hit_rate == 1.0
    assert report.recall_at_k == 1.0
    assert report.answer_term_coverage == 1.0

