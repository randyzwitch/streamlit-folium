from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit.components.v2 as components_v2

_JS_BUNDLE = list(
    (Path(__file__).resolve().parents[1] / "frontend" / "build").glob("index-*.js")
)
_JS_FILE = _JS_BUNDLE[0] if _JS_BUNDLE else None
_JS_CODE = _JS_FILE.read_text() if _JS_FILE is not None else ""

_component = components_v2.component(
    "st_folium_vnext",
    js=_JS_CODE,
    html=" ",
    isolate_styles=False,
)


def _noop():
    pass


def mount_leaflet_component(
    *,
    spec: dict[str, Any],
    key: str | None,
    height: int = 500,
    width: str = "stretch",
):
    return _component(
        key=key,
        data={"spec": spec, "height": height, "width": width},
        default={"center": None, "zoom": None, "bounds": None},
        height=height,
        on_center_change=_noop,
        on_zoom_change=_noop,
        on_bounds_change=_noop,
        on_event_change=_noop,
    )
