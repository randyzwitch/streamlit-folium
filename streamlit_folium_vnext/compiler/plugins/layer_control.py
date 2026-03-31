from __future__ import annotations

import folium

from streamlit_folium_vnext.compiler.context import CompileContext
from streamlit_folium_vnext.compiler.nodes import make_node
from streamlit_folium_vnext.models.spec import MapNode


def compile_layer_control(obj: folium.LayerControl, context: CompileContext) -> MapNode:
    options = dict(obj.options) if hasattr(obj, "options") else {}
    return make_node(
        "layer_control",
        context.allocate_id("layer-control"),
        position=options.get("position", "topright"),
        options=options,
    )
