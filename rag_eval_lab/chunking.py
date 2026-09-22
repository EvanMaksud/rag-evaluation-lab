from __future__ import annotations

import re
from dataclasses import dataclass

from .corpus import Document


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    text: str
    start_token: int
    end_token: int


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 180,
    overlap: int = 40,
) -> list[Chunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[Chunk] = []
    for document in documents:
        tokens = tokenize(document.text)
        if not tokens:
            continue
        stride = chunk_size - overlap
        index = 0
        for start in range(0, len(tokens), stride):
            end = min(start + chunk_size, len(tokens))
            chunk_text = " ".join(tokens[start:end])
            chunks.append(
                Chunk(
                    chunk_id=f"{document.doc_id}::chunk-{index:03d}",
                    doc_id=document.doc_id,
                    title=document.title,
                    text=chunk_text,
                    start_token=start,
                    end_token=end,
                )
            )
            index += 1
            if end == len(tokens):
                break
    return chunks


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+(?:[-']\w+)?|[^\w\s]", text, flags=re.UNICODE)

