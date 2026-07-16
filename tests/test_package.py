from textwrap import dedent


def test_map():
    import folium

    from streamlit_folium import _get_map_string

    map = folium.Map()
    map.render()

    leaflet = _get_map_string(map)
    assert (
        dedent(
            """var map_div = L.map(
                "map_div",
                {
                    center: [0.0, 0.0],
                    crs: L.CRS.EPSG3857,"""
        )
        in leaflet
    )

    assert "var tile_layer_div_0 = L.tileLayer(" in leaflet

    assert ".addTo(map_div);" in leaflet


def test_layer_control():
    import folium

    from streamlit_folium import generate_leaflet_string

    map = folium.Map()
    folium.LayerControl().add_to(map)
    map.render()
    leaflet = generate_leaflet_string(map)
    assert "var tile_layer_div_0 = L.tileLayer(" in leaflet
    assert '"openstreetmap" : tile_layer_div_0,' in leaflet


def test_draw_support():
    import folium
    from folium.plugins import Draw

    from streamlit_folium import _get_map_string

    map = folium.Map()
    Draw(export=True).add_to(map)
    map.render()
    leaflet = _get_map_string(map)
    assert "map_div.on(L.Draw.Event.CREATED, function(e) {" in leaflet
    assert "drawnItems.addLayer(layer);" in leaflet

    assert (
        """map_div.on('draw:created', function(e) {
                drawnItems.addLayer(e.layer);
            });"""
        in leaflet
    )

    assert (
        """var draw_control_div_1 = new L.Control.Draw(
                options
            ).addTo( map_div );"""
        in leaflet
    )

    assert "alert" not in leaflet


def test_map_id():
    import folium

    from streamlit_folium import _get_map_string

    map = folium.Map()
    leaflet = _get_map_string(map)
    assert "var map_div = L.map(" in leaflet


def test_feature_group():
    import folium

    from streamlit_folium import _get_feature_group_string

    fg = folium.FeatureGroup()
    m = folium.Map()

    fg_str = _get_feature_group_string(fg, m)

    assert "var feature_group_feature_group_0 = L.featureGroup(" in fg_str
    assert ".addTo(map_div);" in fg_str


def test_dual_map():
    import folium.plugins

    from streamlit_folium import _get_map_string

    dual_map = folium.plugins.DualMap()
    dual_map.render()
    map_str = _get_map_string(dual_map)

    assert "var map_div = L.map(" in map_str
    assert "var map_div2 = L.map(" in map_str


def test_vector_grid():
    import folium
    from folium.plugins import VectorGridProtobuf

    from streamlit_folium import _get_map_string

    m = folium.Map()
    url = "https://free-{s}.tilehosting.com/data/v3/{z}/{x}/{y}.pbf?token={token}"
    VectorGridProtobuf(url, "test").add_to(m)
    leaflet = _get_map_string(m)
    assert "var vector_grid_protobuf_div_1 = L.vectorGrid.protobuf(" in leaflet


def test_last_object_clicked_count_default():
    import folium

    import streamlit_folium as sf
    from streamlit_folium import st_folium

    original_component_func = sf._component_func
    captured: dict = {}

    def fake_component_func(**kwargs):
        captured.update(kwargs)
        return kwargs.get("default", {})

    try:
        sf._component_func = fake_component_func
        m = folium.Map(location=[0, 0], zoom_start=1)
        result = st_folium(m, returned_objects=["last_object_clicked_count"])
        assert result["last_object_clicked_count"] is None
        assert "last_object_clicked_count" in captured.get("default", {})
    finally:
        sf._component_func = original_component_func


def test_last_object_clicked_count_not_in_default_when_not_requested():
    import folium

    import streamlit_folium as sf
    from streamlit_folium import st_folium

    original_component_func = sf._component_func
    captured: dict = {}

    def fake_component_func(**kwargs):
        captured.update(kwargs)
        return kwargs.get("default", {})

    try:
        sf._component_func = fake_component_func
        m = folium.Map(location=[0, 0], zoom_start=1)
        result = st_folium(m, returned_objects=["last_object_clicked"])
        assert "last_object_clicked_count" not in result
    finally:
        sf._component_func = original_component_func
