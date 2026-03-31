from __future__ import annotations

import folium

from streamlit_folium_vnext.compiler.nodes import make_node


def compile_tile_layer(obj: folium.raster_layers.TileLayer, context):
    return make_node(
        "tile_layer",
        context.allocate_id("tile-layer"),
        url=obj.tiles,
        attribution=obj.options.get("attribution", ""),
        name=obj.layer_name,
        options=dict(obj.options),
    )


def compile_marker(obj: folium.map.Marker, context):
    location = list(obj.location) if obj.location is not None else None
    popup = None
    tooltip = None
    for child in obj._children.values():
        if isinstance(child, folium.map.Popup):
            popup = {
                "html": child.html.render()
                if hasattr(child, "html")
                else getattr(child, "text", None)
            }
        elif isinstance(child, folium.map.Tooltip):
            tooltip = {"text": child.text}

    return make_node(
        "marker",
        context.allocate_id("marker"),
        location=location,
        popup=popup,
        tooltip=tooltip,
        options=dict(obj.options),
    )


def compile_circle_marker(obj: folium.vector_layers.CircleMarker, context):
    location = list(obj.location) if obj.location is not None else None
    return make_node(
        "circle_marker",
        context.allocate_id("circle-marker"),
        location=location,
        radius=obj.options.get("radius"),
        options=dict(obj.options),
    )


def compile_geojson(obj: folium.features.GeoJson, context):
    return make_node(
        "geojson",
        context.allocate_id("geojson"),
        data=obj.data,
        options=dict(obj.options),
    )
