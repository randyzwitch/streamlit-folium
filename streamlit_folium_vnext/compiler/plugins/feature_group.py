from __future__ import annotations

import folium

from streamlit_folium_vnext.compiler.context import CompileContext
from streamlit_folium_vnext.compiler.nodes import make_node
from streamlit_folium_vnext.models.spec import MapNode


def compile_feature_group(obj: folium.FeatureGroup, context: CompileContext) -> MapNode:
    return make_node(
        "feature_group",
        context.allocate_id("feature-group"),
        name=getattr(obj, "layer_name", None),
    )
