from __future__ import annotations

from streamlit_folium_vnext.compiler.nodes import make_node


def compile_layer_control(obj, context):
    options = dict(obj.options) if hasattr(obj, "options") else {}
    return make_node(
        "layer_control",
        context.allocate_id("layer-control"),
        position=options.get("position", "topright"),
        options=options,
    )
