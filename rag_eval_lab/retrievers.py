from __future__ import annotations

from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .chunking import Chunk


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float
    rank: int


class TfidfRetriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        if not chunks:
            raise ValueError("Cannot build a retriever with zero chunks")
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=1,
            stop_words="english",
            sublinear_tf=True,
        )
        self.matrix = self.vectorizer.fit_transform(chunk.text for chunk in chunks)

    def search(self, query: str, k: int = 5) -> list[SearchResult]:
        if k <= 0:
            raise ValueError("k must be positive")
        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.matrix).ravel()
        top_indices = scores.argsort()[::-1][:k]
        return [
            SearchResult(chunk=self.chunks[index], score=float(scores[index]), rank=rank)
            for rank, index in enumerate(top_indices, start=1)
        ]

