from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class MapNode:
    kind: str
    id: str
    props: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class MapSpec:
    version: int = 1
    map: dict[str, Any] = field(default_factory=dict)
    layers: list[MapNode] = field(default_factory=list)
    controls: list[MapNode] = field(default_factory=list)
    plugins: list[MapNode] = field(default_factory=list)
    subscriptions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "map": self.map,
            "layers": [node.to_dict() for node in self.layers],
            "controls": [node.to_dict() for node in self.controls],
            "plugins": [node.to_dict() for node in self.plugins],
            "subscriptions": self.subscriptions,
        }
