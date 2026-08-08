from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .source import SourceCitation


@dataclass
class LatencyBreakdown:
    embedding_ms: Optional[float] = None
    retrieval_ms: Optional[float] = None
    generation_ms: Optional[float] = None
    total_ms: Optional[float] = None


DEFAULT_DISCLAIMER = (
    "Este assistente nao substitui parecer juridico. "
    "As respostas sao baseadas exclusivamente nos documentos indexados."
)

INSUFFICIENT_INFORMATION_TEXT = (
    "Nao encontrei informacao suficiente nos documentos internos indexados para "
    "responder a esta pergunta com seguranca. "
    "Sugiro consultar diretamente os responsaveis pela area: Juridico / Compliance "
    "(DPO), Seguranca da Informacao (CISO) ou Recursos Humanos, conforme o assunto. "
    "Se a duvida for sobre a LGPD ou a ANPD, tambem e possivel consultar os guias e "
    "a FAQ oficiais disponiveis em docs/oficiais."
)


@dataclass
class Answer:
    text: str
    citations: List[SourceCitation] = field(default_factory=list)
    model: str = ""
    retrieval_time_ms: Optional[float] = None
    generation_time_ms: Optional[float] = None
    total_time_ms: Optional[float] = None
    answered_at: datetime = field(default_factory=datetime.utcnow)
    disclaimer: str = DEFAULT_DISCLAIMER
    insufficient_information: bool = False
    latency: LatencyBreakdown = field(default_factory=LatencyBreakdown)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def sources_text(self) -> str:
        if not self.citations:
            return "Nenhuma fonte citada."
        return "\n".join(f"- {c.pretty()}" for c in self.citations)

    def citation_titles(self) -> list[str]:
        seen = set()
        titles = []
        for c in self.citations:
            t = (c.doc_title or "").strip().lower()
            if t and t not in seen:
                seen.add(t)
                titles.append(c.doc_title)
        return titles

    def citation_sections(self) -> list[str]:
        return [c.section for c in self.citations if c.section]

    def pretty_metrics(self) -> str:
        lines = [
            f"  Modelo               : {self.model or 'n/d'}",
            f"  Tempo total    (ms)  : {self.total_time_ms:.1f}" if self.total_time_ms is not None else "  Tempo total    (ms)  : n/d",
        ]
        lat = self.latency
        if lat.embedding_ms is not None:
            lines.append(f"  Tempo embed    (ms)  : {lat.embedding_ms:.1f}")
        if lat.retrieval_ms is not None:
            lines.append(f"  Tempo de busca (ms)  : {lat.retrieval_ms:.1f}")
        if lat.generation_ms is not None:
            lines.append(f"  Tempo de geracao(ms) : {lat.generation_ms:.1f}")
        return "\n".join(lines)

