from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import pytest

from src.domain.answer import (
    DEFAULT_DISCLAIMER,
    INSUFFICIENT_INFORMATION_TEXT,
    Answer,
    LatencyBreakdown,
)
from src.domain.source import SourceCitation
from src.services.qa_service import _build_answer, _is_useful


def _citation(title: str, section: Optional[str] = None, score: float = 0.5) -> SourceCitation:
    return SourceCitation(
        doc_id=title.lower().replace(" ", "_"),
        doc_title=title,
        source="md",
        section=section,
        score=score,
        snippet="",
    )


@dataclass
class FakeSettings:
    retriever_top_k: int = 5
    retriever_score_threshold: float = 0.2


@dataclass
class Paths:
    vector_store_dir: str = "data/vector_store"


class TestAnswerDataclass:
    def test_defaults(self):
        a = Answer(text="teste")
        assert a.text == "teste"
        assert a.citations == []
        assert a.disclaimer == DEFAULT_DISCLAIMER
        assert a.insufficient_information is False
        assert isinstance(a.latency, LatencyBreakdown)

    def test_citation_titles_dedup(self):
        cits = [
            _citation("Política Segurança", "1", 0.9),
            _citation("Política Segurança", "2", 0.8),
            _citation("Código de Ética", "3", 0.7),
        ]
        a = Answer(text="x", citations=cits)
        assert a.citation_titles() == ["Política Segurança", "Código de Ética"]

    def test_sources_text(self):
        cits = [_citation("PSI", "3.2", 0.6)]
        assert "PSI" in Answer(text="x", citations=cits).sources_text()
        assert "3.2" in Answer(text="x", citations=cits).sources_text()


class TestBuildAnswer:
    def test_valid_answer_when_useful(self):
        cits = [_citation("Plano Resposta Incidentes", "Secao 2", 0.7)]
        ans = _build_answer(
            answer_text="O SLA S0 e de 1 hora. Acione o CISO e CTO.",
            citations=cits,
            model="cohere",
            embed_ms=10.0,
            retrieval_ms=300.0,
            generation_ms=1500.0,
            total_ms=1810.0,
        )
        assert ans.insufficient_information is False
        assert ans.latency.embedding_ms == 10.0
        assert ans.latency.retrieval_ms == 300.0
        assert ans.latency.generation_ms == 1500.0
        assert ans.latency.total_ms == 1810.0
        assert "INSUFFICIENT_INFORMATION" not in ans.text
        assert ans.model == "cohere"

    def test_insufficient_when_low_score_citations(self):
        cits = [_citation("Doc Aleatorio", "S1", 0.1)]
        ans = _build_answer(
            answer_text="Resposta qualquer inventada",
            citations=cits,
            model="cohere",
            embed_ms=5.0,
            retrieval_ms=200.0,
            generation_ms=800.0,
            total_ms=1005.0,
        )
        assert ans.insufficient_information is True
        assert ans.text == INSUFFICIENT_INFORMATION_TEXT

    def test_insufficient_when_empty_answer(self):
        cits = [_citation("X", "S", 0.6)]
        ans = _build_answer(
            answer_text="",
            citations=cits,
            model="cohere",
            embed_ms=1.0,
            retrieval_ms=50.0,
            generation_ms=500.0,
            total_ms=551.0,
        )
        assert ans.insufficient_information is True

    def test_pretty_metrics(self):
        cits = [_citation("Y", "Sec", 0.7)]
        ans = _build_answer(
            answer_text="ok",
            citations=cits,
            model="cohere/test",
            embed_ms=12.1,
            retrieval_ms=212.3,
            generation_ms=1530.7,
            total_ms=1755.1,
        )
        rendered = ans.pretty_metrics()
        assert "cohere/test" in rendered
        assert "embed" in rendered
        assert "busca" in rendered
        assert "geracao" in rendered


class TestUsefulCitation:
    def test_threshold(self):
        assert _is_useful(_citation("A", score=0.4)) is True
        assert _is_useful(_citation("A", score=0.35)) is True
        assert _is_useful(_citation("A", score=0.34)) is False
        assert _is_useful(_citation("A", score=None)) is True


class TestAntiHallucinationHeuristics:
    def test_build_answer_flag_when_no_context(self):
        ans = _build_answer(
            answer_text="Eu nao sei mas vou inventar uma politica de RH",
            citations=[],
            model="x",
            embed_ms=1.0,
            retrieval_ms=10.0,
            generation_ms=100.0,
            total_ms=111.0,
        )
        assert ans.insufficient_information is True
        assert ans.text.startswith("Nao encontrei informacao suficiente")
