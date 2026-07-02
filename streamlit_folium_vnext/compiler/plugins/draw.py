from __future__ import annotations

import folium.plugins

from streamlit_folium_vnext.compiler.context import CompileContext
from streamlit_folium_vnext.compiler.nodes import make_node
from streamlit_folium_vnext.models.spec import MapNode


def compile_draw(obj: folium.plugins.Draw, context: CompileContext) -> MapNode:
    return make_node(
        "draw", context.allocate_id("draw"), options=getattr(obj, "options", {})
    )
