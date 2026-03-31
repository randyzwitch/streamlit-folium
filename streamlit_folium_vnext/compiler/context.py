from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CompileContext:
    next_id: int = 0

    def allocate_id(self, prefix: str) -> str:
        self.next_id += 1
        return f"{prefix}-{self.next_id}"
