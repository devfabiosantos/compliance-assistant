from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .source import SourceCitation


@dataclass
class Answer:
    text: str
    citations: List[SourceCitation] = field(default_factory=list)
    model: str = ""
    retrieval_time_ms: Optional[float] = None
    generation_time_ms: Optional[float] = None
    total_time_ms: Optional[float] = None
    answered_at: datetime = field(default_factory=datetime.utcnow)
    disclaimer: str = (
        "Este assistente nao substitui parecer juridico. "
        "As respostas sao baseadas exclusivamente nos documentos indexados."
    )

    def sources_text(self) -> str:
        if not self.citations:
            return "Nenhuma fonte citada."
        return "\n".join(f"- {c.pretty()}" for c in self.citations)
