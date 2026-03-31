from __future__ import annotations

import folium
import streamlit as st
from folium.plugins import Draw

from streamlit_folium_vnext import st_folium_vnext

st.set_page_config(page_title="vnext demo", layout="wide")
st.title("streamlit-folium vnext")

m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
folium.Marker([37.7749, -122.4194], popup="San Francisco", tooltip="SF").add_to(m)
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

result = st_folium_vnext(
    m,
    key="vnext-map",
    height=500,
    subscribe=["click", "moveend", "draw.created", "draw.edited", "draw.deleted"],
)

st.subheader("State")
st.json(
    {
        "center": result.center if result else None,
        "zoom": result.zoom if result else None,
        "bounds": result.bounds if result else None,
        "event": result.event if result else None,
    }
)
