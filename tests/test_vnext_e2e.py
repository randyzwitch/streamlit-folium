from __future__ import annotations

import json

import folium
import folium.vector_layers
from folium.plugins import Draw

from streamlit_folium_vnext import compile_folium


class TestCompilerEdgeCases:
    def test_circle_marker_compiles(self):
        m = folium.Map(location=[0, 0], zoom_start=3)
        folium.CircleMarker(location=[10, 20], radius=15).add_to(m)

        spec = compile_folium(m)
        cm = next(node for node in spec.layers if node.kind == "circle_marker")
        assert cm.props["location"] == [10, 20]
        assert cm.props["radius"] == 15

    def test_multiple_markers(self):
        m = folium.Map(location=[0, 0], zoom_start=3)
        folium.Marker([1, 2]).add_to(m)
        folium.Marker([3, 4]).add_to(m)
        folium.Marker([5, 6]).add_to(m)

        spec = compile_folium(m)
        markers = [node for node in spec.layers if node.kind == "marker"]
        assert len(markers) == 3
        locs = [node.props["location"] for node in markers]
        assert [1, 2] in locs
        assert [3, 4] in locs
        assert [5, 6] in locs

    def test_geojson_preserves_data(self):
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [0, 0]},
                    "properties": {"name": "Origin"},
                }
            ],
        }
        m = folium.Map(location=[0, 0], zoom_start=3)
        folium.GeoJson(geojson_data).add_to(m)

        spec = compile_folium(m)
        gj = next(node for node in spec.layers if node.kind == "geojson")
        assert gj.props["data"]["features"][0]["properties"]["name"] == "Origin"

    def test_tile_layer_default(self):
        m = folium.Map(location=[0, 0], zoom_start=3)

        spec = compile_folium(m)
        tiles = [node for node in spec.layers if node.kind == "tile_layer"]
        assert len(tiles) >= 1
        assert tiles[0].props["url"] is not None

    def test_draw_plugin_with_options(self):
        m = folium.Map(location=[0, 0], zoom_start=3)
        Draw(export=True, draw_options={"polyline": False}).add_to(m)

        spec = compile_folium(m)
        draw = next(p for p in spec.plugins if p.kind == "draw")
        assert draw.props["options"] is not None

    def test_feature_group_with_children(self):
        m = folium.Map(location=[0, 0], zoom_start=3)
        fg = folium.FeatureGroup(name="test-group")
        folium.Marker([1, 2]).add_to(fg)
        fg.add_to(m)

        spec = compile_folium(m)
        fg_node = next(node for node in spec.layers if node.kind == "feature_group")
        assert fg_node.props["name"] == "test-group"

    def test_layer_control_position(self):
        m = folium.Map(location=[0, 0], zoom_start=3)
        folium.LayerControl(position="topleft").add_to(m)

        spec = compile_folium(m)
        lc = next(c for c in spec.controls if c.kind == "layer_control")
        assert lc.props["position"] == "topleft"

    def test_subscriptions_passed_through(self):
        m = folium.Map(location=[0, 0], zoom_start=3)
        spec = compile_folium(m, subscribe=["click", "moveend", "draw.created"])
        assert spec.subscriptions == ["click", "moveend", "draw.created"]

    def test_no_subscriptions_defaults_empty(self):
        m = folium.Map(location=[0, 0], zoom_start=3)
        spec = compile_folium(m)
        assert spec.subscriptions == []

    def test_spec_serialization_roundtrip(self):
        m = folium.Map(location=[37.77, -122.42], zoom_start=12)
        folium.Marker([37.77, -122.42], popup="test", tooltip="tip").add_to(m)
        folium.GeoJson({"type": "FeatureCollection", "features": []}).add_to(m)
        folium.LayerControl().add_to(m)
        Draw().add_to(m)

        spec = compile_folium(m, subscribe=["click"])
        d = spec.to_dict()

        assert json.loads(json.dumps(d)) == d

    def test_unique_ids(self):
        m = folium.Map(location=[0, 0], zoom_start=3)
        folium.Marker([1, 2]).add_to(m)
        folium.Marker([3, 4]).add_to(m)
        folium.CircleMarker([5, 6]).add_to(m)
        folium.GeoJson({"type": "FeatureCollection", "features": []}).add_to(m)

        spec = compile_folium(m)
        ids = [node.id for node in spec.layers]
        assert len(ids) == len(set(ids)), f"Duplicate IDs found: {ids}"

    def test_full_demo_compiles_without_error(self):
        m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
        folium.Marker([37.7749, -122.4194], popup="San Francisco", tooltip="SF").add_to(
            m
        )
        folium.GeoJson(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [-122.4194, 37.7749],
                        },
                        "properties": {"name": "SF"},
                    }
                ],
            }
        ).add_to(m)
        folium.LayerControl().add_to(m)
        Draw(export=False).add_to(m)

        spec = compile_folium(
            m,
            subscribe=[
                "click",
                "moveend",
                "draw.created",
                "draw.edited",
                "draw.deleted",
            ],
        )
        d = spec.to_dict()

        assert d["version"] == 1
        assert d["map"]["center"] == [37.7749, -122.4194]
        assert d["map"]["zoom"] == 12
        assert len(d["layers"]) >= 3
        assert len(d["controls"]) >= 1
        assert len(d["plugins"]) >= 1
        assert len(d["subscriptions"]) == 5

        json.dumps(d)


class TestAppTestE2E:
    def test_vnext_demo_runs_without_error(self):
        import pytest

        pytest.skip(
            "CCv2 bidi components raise TypeError in Streamlit AppTest headless runner "
            "(known incompatibility with BidiComponentProto in test mode)"
        )
