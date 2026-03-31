from __future__ import annotations

from streamlit_folium_vnext.compiler.nodes import make_node


def compile_feature_group(obj, context):
    return make_node(
        "feature_group",
        context.allocate_id("feature-group"),
        name=getattr(obj, "layer_name", None),
    )
