from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

from src.domain.document import Chunk
from src.domain.source import SourceCitation
from src.retrieval.vector_store import VectorStore


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float
    rank: int

    def to_citation(self) -> SourceCitation:
        return SourceCitation(
            doc_id=self.chunk.doc_id,
            doc_title=self.chunk.doc_title,
            source=self.chunk.source,
            page=self.chunk.page,
            section=self.chunk.section,
            score=self.score,
            snippet=self.chunk.content[:240],
        )


class Retriever:
    def __init__(
        self,
        vector_store: VectorStore,
        top_k: int = 5,
        score_threshold: float = 0.0,
    ) -> None:
        self._vector_store = vector_store
        self._top_k = top_k
        self._score_threshold = score_threshold

    def retrieve(self, query_vector: Sequence[float]) -> List[RetrievedChunk]:
        raw = self._vector_store.search(query_vector, top_k=self._top_k)
        ranked: List[RetrievedChunk] = []
        for rank, (chunk, score) in enumerate(raw, start=1):
            if self._score_threshold and score < self._score_threshold:
                continue
            ranked.append(RetrievedChunk(chunk=chunk, score=score, rank=rank))
        return ranked
