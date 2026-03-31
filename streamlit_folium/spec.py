from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class PluginSpec:
    kind: str
    script: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AssetSpec:
    js: list[str] = field(default_factory=list)
    css: list[str] = field(default_factory=list)

    def to_payload(self) -> dict[str, list[str]]:
        return {"js": self.js, "css": self.css}


@dataclass
class MapSpec:
    html: str
    header: str
    script: str
    map_id: str
    defaults: dict[str, Any]
    assets: AssetSpec
    plugins: list[PluginSpec] = field(default_factory=list)

    def to_payload(self) -> dict[str, Any]:
        return {
            "html": self.html,
            "header": self.header,
            "script": self.script,
            "id": self.map_id,
            "default": self.defaults,
            "assets": self.assets.to_payload(),
            "plugins": [plugin.to_payload() for plugin in self.plugins],
        }
