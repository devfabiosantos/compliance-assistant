from __future__ import annotations

import logging
import time
from typing import List

from src.config.settings import Settings
from src.domain.answer import (
    DEFAULT_DISCLAIMER,
    INSUFFICIENT_INFORMATION_TEXT,
    Answer,
    LatencyBreakdown,
)
from src.domain.question import Question
from src.domain.source import SourceCitation
from src.providers.base import ChatProvider
from src.providers.base import EmbeddingProvider
from src.retrieval.retriever import Retriever, RetrievedChunk
from src.retrieval.vector_store import VectorStore

logger = logging.getLogger(__name__)


_MIN_USEFUL_SCORE = 0.35
_MIN_USEFUL_CHUNKS = 1


def _is_useful(citation: SourceCitation) -> bool:
    if citation.score is None:
        return True
    return citation.score >= _MIN_USEFUL_SCORE


def _build_answer(
    *,
    answer_text: str,
    citations: List[SourceCitation],
    model: str,
    embed_ms: float,
    retrieval_ms: float,
    generation_ms: float,
    total_ms: float,
    metadata: dict | None = None,
) -> Answer:
    useful = [c for c in citations if _is_useful(c)]
    insufficient = (
        len(useful) < _MIN_USEFUL_CHUNKS
        or not answer_text.strip()
        or "INSUFFICIENT_INFORMATION" in answer_text
    )

    if insufficient:
        final_text = INSUFFICIENT_INFORMATION_TEXT
    else:
        final_text = answer_text.strip()

    return Answer(
        text=final_text,
        citations=citations,
        model=model,
        retrieval_time_ms=round(retrieval_ms, 1),
        generation_time_ms=round(generation_ms, 1),
        total_time_ms=round(total_ms, 1),
        disclaimer=DEFAULT_DISCLAIMER,
        insufficient_information=insufficient,
        latency=LatencyBreakdown(
            embedding_ms=round(embed_ms, 1),
            retrieval_ms=round(retrieval_ms, 1),
            generation_ms=round(generation_ms, 1),
            total_ms=round(total_ms, 1),
        ),
        metadata=dict(metadata or {}),
    )


class QAService:
    def __init__(
        self,
        settings: Settings,
        chat_provider: ChatProvider,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore | None = None,
        retriever: Retriever | None = None,
    ) -> None:
        self._settings = settings
        self._chat_provider = chat_provider
        self._embedding_provider = embedding_provider
        if vector_store is None:
            vector_store = VectorStore(
                directory=settings.paths.vector_store_dir,
                embedding_dimension=0,
                embedding_model=embedding_provider.name,
            )
            vector_store.load()
        self._vector_store = vector_store
        if retriever is None:
            retriever = Retriever(
                vector_store=self._vector_store,
                top_k=settings.retriever_top_k,
                score_threshold=settings.retriever_score_threshold,
            )
        self._retriever = retriever

    def answer(self, question: str) -> Answer:
        start = time.perf_counter()
        q = Question(text=question)

        t_embed = time.perf_counter()
        query_vector = self._embedding_provider.embed_query(q.text)
        embed_ms = (time.perf_counter() - t_embed) * 1000

        t_ret = time.perf_counter()
        retrieved: List[RetrievedChunk] = self._retriever.retrieve(query_vector)
        retrieval_ms = (time.perf_counter() - t_ret) * 1000

        citations: List[SourceCitation] = [r.to_citation() for r in retrieved]
        context_chunks = [r.chunk.content for r in retrieved]

        logger.info(
            "retrieval concluido",
            extra={
                "question": q.text,
                "chunks": len(retrieved),
                "embedding_ms": round(embed_ms, 1),
                "retrieval_ms": round(retrieval_ms, 1),
            },
        )

        t_gen = time.perf_counter()
        answer_text = self._chat_provider.answer_with_context(
            question=q.text,
            context_chunks=context_chunks,
            citations=citations,
        )
        generation_ms = (time.perf_counter() - t_gen) * 1000
        total_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "resposta gerada",
            extra={
                "model": self._chat_provider.name,
                "generation_ms": round(generation_ms, 1),
                "total_ms": round(total_ms, 1),
            },
        )

        return _build_answer(
            answer_text=answer_text,
            citations=citations,
            model=self._chat_provider.name,
            embed_ms=embed_ms,
            retrieval_ms=retrieval_ms,
            generation_ms=generation_ms,
            total_ms=total_ms,
            metadata={
                "question": q.text,
                "useful_citations": len([c for c in citations if _is_useful(c)]),
                "total_citations": len(citations),
            },
        )
