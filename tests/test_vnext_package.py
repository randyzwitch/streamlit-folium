from streamlit_folium_vnext import compile_folium


def test_compile_empty_map():
    import folium

    spec = compile_folium(folium.Map(location=[10, 20], zoom_start=4))

    payload = spec.to_dict()
    assert payload["version"] == 1
    assert payload["map"]["center"] == [10, 20]
    assert payload["map"]["zoom"] == 4


def test_compile_core_layers_draw_and_controls():
    import folium
    from folium.plugins import Draw

    m = folium.Map(location=[0, 0], zoom_start=3)
    fg = folium.FeatureGroup(name="Cities")
    fg.add_to(m)
    folium.Marker(location=[1, 2], popup="Hello", tooltip="There").add_to(m)
    folium.GeoJson({"type": "FeatureCollection", "features": []}).add_to(m)
    folium.LayerControl(position="bottomleft").add_to(m)
    Draw().add_to(m)

    spec = compile_folium(m, subscribe=["click", "draw.created"])
    payload = spec.to_dict()

    kinds = [layer["kind"] for layer in payload["layers"]]
    assert "feature_group" in kinds
    assert "marker" in kinds
    assert "geojson" in kinds
    assert payload["controls"][0]["kind"] == "layer_control"
    assert payload["plugins"][0]["kind"] == "draw"
    assert payload["subscriptions"] == ["click", "draw.created"]


def test_marker_popup_and_tooltip_are_serialized():
    import folium

    m = folium.Map(location=[0, 0], zoom_start=3)
    folium.Marker(location=[1, 2], popup="Hello", tooltip="There").add_to(m)

    spec = compile_folium(m)
    marker = next(
        layer for layer in spec.to_dict()["layers"] if layer["kind"] == "marker"
    )

    assert marker["props"]["location"] == [1, 2]
    assert marker["props"]["popup"]["html"] is not None
    assert marker["props"]["tooltip"]["text"] == "There"
