from __future__ import annotations

import folium
import streamlit as st

from streamlit_folium_vnext import st_folium_vnext

st.title("Multiple Maps")
st.caption("Two independent maps side by side. Each maintains its own state.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tokyo")
    m1 = folium.Map(location=[35.6762, 139.6503], zoom_start=12)
    folium.Marker([35.6762, 139.6503], tooltip="Tokyo Tower area").add_to(m1)
    folium.Marker([35.6586, 139.7454], tooltip="Ginza").add_to(m1)
    r1 = st_folium_vnext(m1, key="map-tokyo", height=400)
    if r1 and r1.center:
        st.caption(f"Center: {r1.center[0]:.4f}, {r1.center[1]:.4f} | Zoom: {r1.zoom}")
    with st.expander("Show code"):
        st.code(
            """\
m1 = folium.Map(location=[35.6762, 139.6503], zoom_start=12)
folium.Marker([35.6762, 139.6503], tooltip="Tokyo Tower area").add_to(m1)
r1 = st_folium_vnext(m1, key="map-tokyo", height=400)
""",
            language="python",
        )

with col2:
    st.subheader("London")
    m2 = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
    folium.Marker([51.5074, -0.1278], tooltip="Big Ben area").add_to(m2)
    folium.Marker([51.5014, -0.1419], tooltip="Buckingham Palace").add_to(m2)
    r2 = st_folium_vnext(m2, key="map-london", height=400)
    if r2 and r2.center:
        st.caption(f"Center: {r2.center[0]:.4f}, {r2.center[1]:.4f} | Zoom: {r2.zoom}")
    with st.expander("Show code"):
        st.code(
            """\
m2 = folium.Map(location=[51.5074, -0.1278], zoom_start=12)
folium.Marker([51.5074, -0.1278], tooltip="Big Ben area").add_to(m2)
r2 = st_folium_vnext(m2, key="map-london", height=400)
""",
            language="python",
        )
