from __future__ import annotations

import folium
import folium.plugins

from streamlit_folium_vnext.compiler.context import CompileContext
from streamlit_folium_vnext.compiler.nodes import make_node
from streamlit_folium_vnext.models.spec import MapNode


def compile_tile_layer(
    obj: folium.raster_layers.TileLayer, context: CompileContext
) -> MapNode:
    return make_node(
        "tile_layer",
        context.allocate_id("tile-layer"),
        url=obj.tiles,
        attribution=obj.options.get("attribution", ""),
        name=obj.layer_name,
        options=dict(obj.options),
    )


def compile_marker(obj: folium.map.Marker, context: CompileContext) -> MapNode:
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


def compile_circle_marker(
    obj: folium.vector_layers.CircleMarker, context: CompileContext
) -> MapNode:
    location = list(obj.location) if obj.location is not None else None
    return make_node(
        "circle_marker",
        context.allocate_id("circle-marker"),
        location=location,
        radius=obj.options.get("radius"),
        options=dict(obj.options),
    )


def compile_geojson(obj: folium.features.GeoJson, context: CompileContext) -> MapNode:
    return make_node(
        "geojson",
        context.allocate_id("geojson"),
        data=obj.data,
        options=dict(obj.options),
    )


def _extract_tooltip_popup(obj: object) -> tuple[dict | None, dict | None]:
    tooltip = None
    popup = None
    for child in getattr(obj, "_children", {}).values():
        if isinstance(child, folium.map.Popup):
            popup = {
                "html": child.html.render()
                if hasattr(child, "html")
                else getattr(child, "text", None)
            }
        elif isinstance(child, folium.map.Tooltip):
            tooltip = {"text": child.text}
    return tooltip, popup


def compile_circle(
    obj: folium.vector_layers.Circle, context: CompileContext
) -> MapNode:
    location = list(obj.location) if obj.location is not None else None
    tooltip, popup = _extract_tooltip_popup(obj)
    return make_node(
        "circle",
        context.allocate_id("circle"),
        location=location,
        tooltip=tooltip,
        popup=popup,
        options=dict(obj.options),
    )


def compile_polyline(
    obj: folium.vector_layers.PolyLine, context: CompileContext
) -> MapNode:
    locations = [list(loc) for loc in obj.locations] if obj.locations else []
    tooltip, popup = _extract_tooltip_popup(obj)
    return make_node(
        "polyline",
        context.allocate_id("polyline"),
        locations=locations,
        tooltip=tooltip,
        popup=popup,
        options=dict(obj.options),
    )


def compile_polygon(
    obj: folium.vector_layers.Polygon, context: CompileContext
) -> MapNode:
    locations = [list(loc) for loc in obj.locations] if obj.locations else []
    tooltip, popup = _extract_tooltip_popup(obj)
    return make_node(
        "polygon",
        context.allocate_id("polygon"),
        locations=locations,
        tooltip=tooltip,
        popup=popup,
        options=dict(obj.options),
    )


def compile_marker_cluster(
    obj: folium.plugins.MarkerCluster, context: CompileContext
) -> MapNode:
    markers = []
    for child in obj._children.values():
        if not isinstance(child, folium.map.Marker):
            continue
        location = list(child.location) if child.location is not None else None
        tooltip_text = None
        popup_html = None
        for grandchild in child._children.values():
            if isinstance(grandchild, folium.map.Popup):
                popup_html = (
                    grandchild.html.render()
                    if hasattr(grandchild, "html")
                    else getattr(grandchild, "text", None)
                )
            elif isinstance(grandchild, folium.map.Tooltip):
                tooltip_text = grandchild.text
        markers.append(
            {"location": location, "tooltip": tooltip_text, "popup": popup_html}
        )
    return make_node(
        "marker_cluster",
        context.allocate_id("marker-cluster"),
        markers=markers,
        options=dict(obj.options),
    )


def compile_heat(obj: folium.plugins.HeatMap, context: CompileContext) -> MapNode:
    return make_node(
        "heat",
        context.allocate_id("heat"),
        data=obj.data,
        options=dict(obj.options),
    )
