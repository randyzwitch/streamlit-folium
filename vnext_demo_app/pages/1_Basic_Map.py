from __future__ import annotations

import folium
import streamlit as st

from streamlit_folium_vnext import st_folium_vnext

st.set_page_config(page_title="Basic Map", layout="wide")
st.title("Basic Map")
st.caption("Pan, zoom, and interact. The map should NOT flicker.")

m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

folium.Marker(
    [37.7749, -122.4194],
    popup="<b>San Francisco</b><br>City Hall area",
    tooltip="SF City Hall",
).add_to(m)

folium.Marker(
    [37.7849, -122.4094],
    popup="Chinatown",
    tooltip="Chinatown",
).add_to(m)

folium.Marker(
    [37.7694, -122.4862],
    popup="Golden Gate Park",
    tooltip="GG Park",
).add_to(m)

folium.CircleMarker(
    [37.8024, -122.4058],
    radius=8,
    color="red",
    fill=True,
    fill_color="red",
    fill_opacity=0.6,
    popup="Fisherman's Wharf",
    tooltip="Wharf",
).add_to(m)

folium.LayerControl().add_to(m)

result = st_folium_vnext(m, key="basic-map", height=500)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Center Lat", f"{result.center[0]:.4f}" if result and result.center else "—"
    )
with col2:
    st.metric(
        "Center Lng", f"{result.center[1]:.4f}" if result and result.center else "—"
    )
with col3:
    st.metric("Zoom", result.zoom if result and result.zoom else "—")

if result and result.bounds:
    st.caption(
        f"Bounds: SW({result.bounds[0][0]:.4f}, {result.bounds[0][1]:.4f}) "
        f"NE({result.bounds[1][0]:.4f}, {result.bounds[1][1]:.4f})"
    )

with st.expander("Show code"):
    st.code(
        """\
import folium
import streamlit as st
from streamlit_folium_vnext import st_folium_vnext

m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
folium.Marker([37.7749, -122.4194], tooltip="SF City Hall").add_to(m)
folium.CircleMarker([37.8024, -122.4058], radius=8, color="red",
                    fill=True, tooltip="Wharf").add_to(m)
folium.LayerControl().add_to(m)

result = st_folium_vnext(m, key="basic-map", height=500)
# result.center, result.zoom, result.bounds available immediately
""",
        language="python",
    )
