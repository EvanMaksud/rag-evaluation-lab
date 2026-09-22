from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_EXTENSIONS = {".md", ".markdown", ".txt"}


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    text: str
    path: Path


def load_corpus(root: str | Path) -> list[Document]:
    corpus_root = Path(root)
    if not corpus_root.exists():
        raise FileNotFoundError(f"Corpus folder does not exist: {corpus_root}")

    documents: list[Document] = []
    for path in sorted(corpus_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        text = normalize_text(path.read_text(encoding="utf-8", errors="replace"))
        if not text:
            continue
        title = infer_title(path, text)
        documents.append(Document(path.stem, title, text, path))

    if not documents:
        raise ValueError(f"No Markdown or text documents found in {corpus_root}")
    return documents


def infer_title(path: Path, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

