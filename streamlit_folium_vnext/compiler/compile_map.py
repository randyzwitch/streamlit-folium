from __future__ import annotations

import folium
import folium.plugins

from streamlit_folium_vnext.compiler.context import CompileContext
from streamlit_folium_vnext.compiler.plugins import (
    compile_draw,
    compile_feature_group,
    compile_layer_control,
)
from streamlit_folium_vnext.compiler.plugins.map_objects import (
    compile_circle,
    compile_circle_marker,
    compile_geojson,
    compile_marker,
    compile_polygon,
    compile_polyline,
    compile_tile_layer,
)
from streamlit_folium_vnext.compiler.registry import CompilerRegistry
from streamlit_folium_vnext.models.spec import MapSpec

registry = CompilerRegistry()
registry.register(folium.raster_layers.TileLayer, compile_tile_layer)
registry.register(folium.map.Marker, compile_marker)
registry.register(folium.vector_layers.CircleMarker, compile_circle_marker)
registry.register(folium.vector_layers.Circle, compile_circle)
registry.register(folium.vector_layers.PolyLine, compile_polyline)
registry.register(folium.vector_layers.Polygon, compile_polygon)
registry.register(folium.features.GeoJson, compile_geojson)
registry.register(folium.FeatureGroup, compile_feature_group)
registry.register(folium.LayerControl, compile_layer_control)
registry.register(folium.plugins.Draw, compile_draw)


def compile_folium_map(
    obj: folium.Map, *, subscribe: list[str] | None = None
) -> MapSpec:
    context = CompileContext()
    spec = MapSpec(
        map={
            "id": context.allocate_id("map"),
            "center": list(obj.location),
            "zoom": obj.options.get("zoom") or obj.options.get("zoomStart"),
            "options": dict(obj.options),
        },
        subscriptions=subscribe or [],
    )

    for child in obj._children.values():
        handler = registry.resolve(child)
        if handler is None:
            continue
        node = handler(child, context)
        match node.kind:
            case (
                "tile_layer"
                | "marker"
                | "circle_marker"
                | "circle"
                | "polyline"
                | "polygon"
                | "geojson"
                | "feature_group"
            ):
                spec.layers.append(node)
            case "layer_control":
                spec.controls.append(node)
            case _:
                spec.plugins.append(node)

    return spec
