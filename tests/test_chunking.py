from rag_eval_lab.chunking import chunk_documents
from rag_eval_lab.corpus import Document


def test_chunk_documents_uses_overlap(tmp_path):
    document = Document(
        doc_id="doc",
        title="Doc",
        text="one two three four five six seven eight nine ten",
        path=tmp_path / "doc.md",
    )

    chunks = chunk_documents([document], chunk_size=4, overlap=2)

    assert [chunk.text for chunk in chunks] == [
        "one two three four",
        "three four five six",
        "five six seven eight",
        "seven eight nine ten",
    ]


def test_chunk_documents_rejects_invalid_overlap(tmp_path):
    document = Document("doc", "Doc", "one two", tmp_path / "doc.md")

    try:
        chunk_documents([document], chunk_size=4, overlap=4)
    except ValueError as exc:
        assert "overlap" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

