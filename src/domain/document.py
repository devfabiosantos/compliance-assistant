from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Document:
    doc_id: str
    title: str
    source: str
    content: str
    category: str = "uncategorized"
    metadata: Dict[str, Any] = field(default_factory=dict)
    file_path: Optional[Path] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @classmethod
    def from_text(
        cls,
        title: str,
        content: str,
        *,
        source: str,
        category: str = "uncategorized",
        metadata: Optional[Dict[str, Any]] = None,
        file_path: Optional[Path] = None,
    ) -> "Document":
        metadata = metadata or {}
        return cls(
            doc_id=f"{source}/{title}".lower().replace(" ", "_"),
            title=title,
            source=source,
            content=content,
            category=category,
            metadata=metadata,
            file_path=file_path,
        )


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    doc_title: str
    source: str
    content: str
    index: int
    page: Optional[int] = None
    section: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
