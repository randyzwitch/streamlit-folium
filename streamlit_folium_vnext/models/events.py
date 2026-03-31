from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MapEvent:
    type: str
    payload: dict[str, Any] = field(default_factory=dict)
