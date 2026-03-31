from __future__ import annotations

from copy import deepcopy
from typing import Any

import folium
import streamlit as st

from streamlit_folium_vnext.compiler import compile_folium_map
from streamlit_folium_vnext.component import mount_leaflet_component
from streamlit_folium_vnext.models.spec import MapSpec

_DEFAULT_ACCUMULATORS: dict[str, dict[str, Any]] = {
    "click": {
        "key": "clicks",
        "initial": [],
        "mode": "append",
        "extract": lambda e: e["payload"],
    },
    "draw.created": {
        "key": "drawn_features",
        "initial": [],
        "mode": "append",
        "extract": lambda e: e["payload"].get("geojson"),
    },
    "draw.edited": {
        "key": "drawn_features",
        "initial": [],
        "mode": "replace",
        "extract": lambda e: e["payload"].get("features", []),
    },
    "draw.deleted": {
        "key": "drawn_features",
        "initial": [],
        "mode": "replace",
        "extract": lambda e: e["payload"].get("features", []),
    },
}


def _session_key(component_key: str | None) -> str:
    return f"_stf_vnext_state_{component_key or 'default'}"


def _accumulate(
    component_key: str | None, event: dict[str, Any] | None, state_spec: dict[str, Any]
) -> dict[str, Any]:
    sk = _session_key(component_key)
    if sk not in st.session_state:
        st.session_state[sk] = deepcopy(state_spec)

    acc: dict[str, Any] = st.session_state[sk]

    if event is None or not isinstance(event, dict):
        return acc

    event_type = event.get("type", "")
    cfg = _DEFAULT_ACCUMULATORS.get(event_type)
    if cfg is None:
        return acc

    target_key = cfg["key"]
    if target_key not in acc:
        return acc

    value = cfg["extract"](event)
    if cfg["mode"] == "append":
        acc[target_key] = acc[target_key] + [value]
    elif cfg["mode"] == "replace":
        acc[target_key] = list(value) if isinstance(value, list) else [value]

    st.session_state[sk] = acc
    return acc


class FoliumResult:
    def __init__(self, raw_result: Any, accumulated: dict[str, Any] | None = None):
        self._raw = raw_result
        self._accumulated = accumulated or {}

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        if name == "state":
            return self._accumulated
        return getattr(self._raw, name)

    def __bool__(self) -> bool:
        return bool(self._raw)

    def __repr__(self) -> str:
        return f"FoliumResult(raw={self._raw!r}, state={self._accumulated!r})"


def compile_folium(obj: folium.Map, *, subscribe: list[str] | None = None) -> MapSpec:
    return compile_folium_map(obj, subscribe=subscribe)


def st_leaflet(
    spec: MapSpec,
    *,
    key: str | None = None,
    height: int = 500,
    width: str = "stretch",
    state: dict[str, Any] | None = None,
):
    d = spec.to_dict()
    if key is not None:
        d["map"]["id"] = key
    raw = mount_leaflet_component(
        spec=d,
        key=key,
        height=height,
        width=width,
    )
    if state is not None:
        event = getattr(raw, "event", None)
        acc = _accumulate(key, event, state)
        return FoliumResult(raw, acc)
    return raw


def st_folium_vnext(
    obj: folium.Map,
    *,
    key: str | None = None,
    height: int = 500,
    width: str = "stretch",
    subscribe: list[str] | None = None,
    state: dict[str, Any] | None = None,
):
    spec = compile_folium(obj, subscribe=subscribe)
    return st_leaflet(spec, key=key, height=height, width=width, state=state)
