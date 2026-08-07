from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Sequence

from src.domain.source import SourceCitation


class ChatProvider(ABC):
    name: str

    @abstractmethod
    def answer_with_context(
        self,
        question: str,
        context_chunks: Sequence[str],
        citations: Sequence[SourceCitation],
    ) -> str:
        raise NotImplementedError


class EmbeddingProvider(ABC):
    name: str
    dimension: int

    @abstractmethod
    def embed_documents(self, texts: Sequence[str]) -> List[List[float]]:
        raise NotImplementedError

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        raise NotImplementedError
