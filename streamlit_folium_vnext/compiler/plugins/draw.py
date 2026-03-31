from __future__ import annotations

from streamlit_folium_vnext.compiler.nodes import make_node


def compile_draw(obj, context):
    return make_node(
        "draw", context.allocate_id("draw"), options=getattr(obj, "options", {})
    )
