from __future__ import annotations

from streamlit_folium_vnext.models.spec import MapNode


def make_node(kind: str, node_id: str, **props) -> MapNode:
    return MapNode(kind=kind, id=node_id, props=props)
