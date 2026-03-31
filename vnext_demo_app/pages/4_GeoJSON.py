from __future__ import annotations

import folium
import streamlit as st

from streamlit_folium_vnext import st_folium_vnext

st.set_page_config(page_title="GeoJSON", layout="wide")
st.title("GeoJSON Features")
st.caption("Various GeoJSON geometries rendered on a map.")

m = folium.Map(location=[45.0, -100.0], zoom_start=4)

geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-105.0, 40.0],
                        [-100.0, 40.0],
                        [-100.0, 45.0],
                        [-105.0, 45.0],
                        [-105.0, 40.0],
                    ]
                ],
            },
            "properties": {"name": "Wyoming-ish", "pop": 580000},
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-90.0, 35.0],
                    [-85.0, 38.0],
                    [-80.0, 36.0],
                    [-75.0, 40.0],
                ],
            },
            "properties": {"name": "A winding path"},
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-95.0, 38.0],
            },
            "properties": {"name": "Kansas"},
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": [
                    [-112.0, 33.4],
                    [-111.9, 33.5],
                    [-112.1, 33.3],
                ],
            },
            "properties": {"name": "Phoenix area"},
        },
    ],
}

folium.GeoJson(
    geojson_data,
    name="features",
    tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Name:"]),
).add_to(m)

folium.LayerControl().add_to(m)

result = st_folium_vnext(m, key="geojson-map", height=500)

st.subheader("State")
col1, col2 = st.columns(2)
with col1:
    st.metric("Zoom", result.zoom if result and result.zoom else "—")
with col2:
    if result and result.center:
        st.metric("Center", f"{result.center[0]:.2f}, {result.center[1]:.2f}")

with st.expander("Show code"):
    st.code(
        """\
import folium
import streamlit as st
from streamlit_folium_vnext import st_folium_vnext

m = folium.Map(location=[45.0, -100.0], zoom_start=4)

geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature",
         "geometry": {"type": "Polygon", "coordinates": [[...]]},
         "properties": {"name": "Wyoming-ish"}},
        {"type": "Feature",
         "geometry": {"type": "LineString", "coordinates": [...]},
         "properties": {"name": "A winding path"}},
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [-95.0, 38.0]},
         "properties": {"name": "Kansas"}},
    ],
}

folium.GeoJson(geojson_data, name="features",
               tooltip=folium.GeoJsonTooltip(fields=["name"])).add_to(m)
folium.LayerControl().add_to(m)

result = st_folium_vnext(m, key="geojson-map", height=500)
""",
        language="python",
    )
