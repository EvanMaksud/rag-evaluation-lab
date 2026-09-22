from pathlib import Path

from rag_eval_lab.cli import main


def test_cli_writes_markdown_report(tmp_path: Path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "doc.md").write_text("# Doc\nRetrieval quality should be measured.", encoding="utf-8")
    questions = tmp_path / "questions.jsonl"
    questions.write_text(
        '{"id":"q1","question":"What should be measured?",'
        '"relevant_doc_ids":["doc"],"answer_terms":["retrieval"]}\n',
        encoding="utf-8",
    )
    output = tmp_path / "report.md"

    exit_code = main(["evaluate", str(corpus), str(questions), "--output", str(output)])

    assert exit_code == 0
    assert "RAG Retrieval Evaluation Report" in output.read_text(encoding="utf-8")

