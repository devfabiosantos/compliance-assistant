from __future__ import annotations

import logging
import time
from typing import List

from src.config.settings import Settings
from src.domain.answer import Answer
from src.domain.question import Question
from src.domain.source import SourceCitation
from src.providers.base import ChatProvider
from src.providers.base import EmbeddingProvider
from src.retrieval.retriever import Retriever, RetrievedChunk
from src.retrieval.vector_store import VectorStore

logger = logging.getLogger(__name__)


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

        t0 = time.perf_counter()
        query_vector = self._embedding_provider.embed_query(q.text)
        retrieved: List[RetrievedChunk] = self._retriever.retrieve(query_vector)
        retrieval_time_ms = (time.perf_counter() - t0) * 1000

        citations: List[SourceCitation] = [r.to_citation() for r in retrieved]
        context_chunks = [r.chunk.content for r in retrieved]

        logger.info(
            "retrieval concluido",
            extra={
                "question": q.text,
                "chunks": len(retrieved),
                "retrieval_time_ms": round(retrieval_time_ms, 1),
            },
        )

        t1 = time.perf_counter()
        answer_text = self._chat_provider.answer_with_context(
            question=q.text,
            context_chunks=context_chunks,
            citations=citations,
        )
        generation_time_ms = (time.perf_counter() - t1) * 1000
        total_time_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "resposta gerada",
            extra={
                "model": self._chat_provider.name,
                "generation_time_ms": round(generation_time_ms, 1),
                "total_time_ms": round(total_time_ms, 1),
            },
        )

        return Answer(
            text=answer_text,
            citations=citations,
            model=self._chat_provider.name,
            retrieval_time_ms=round(retrieval_time_ms, 1),
            generation_time_ms=round(generation_time_ms, 1),
            total_time_ms=round(total_time_ms, 1),
        )
