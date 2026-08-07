from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass
class Question:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    asked_at: datetime = field(default_factory=datetime.utcnow)
