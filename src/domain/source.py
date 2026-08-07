from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SourceCitation:
    doc_id: str
    doc_title: str
    source: str
    page: Optional[int] = None
    section: Optional[str] = None
    score: Optional[float] = None
    snippet: str = ""

    def pretty(self) -> str:
        parts = [self.doc_title]
        if self.page is not None:
            parts.append(f"Pagina {self.page}")
        if self.section:
            parts.append(f"Secao {self.section}")
        if self.score is not None:
            parts.append(f"score={self.score:.3f}")
        return " — ".join(parts)
