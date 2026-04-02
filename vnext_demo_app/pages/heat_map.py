from __future__ import annotations

import random

import folium
import folium.plugins
import streamlit as st

from streamlit_folium_vnext import st_folium_vnext

st.title("Heat Map")
st.caption("Visualise point density with a smooth heatmap layer.")

col1, col2, col3 = st.columns(3)
with col1:
    radius = st.slider("Radius", 5, 40, 20)
with col2:
    blur = st.slider("Blur", 5, 30, 15)
with col3:
    min_opacity = st.slider("Min opacity", 0.1, 1.0, 0.4, step=0.05)

random.seed(42)

BASE_CLUSTERS = [
    (51.505, -0.09, 300),
    (51.52, -0.11, 200),
    (51.49, -0.07, 150),
    (48.8566, 2.3522, 250),
    (48.87, 2.37, 180),
    (52.52, 13.405, 220),
    (52.50, 13.42, 160),
    (40.7128, -74.006, 280),
    (40.72, -73.99, 190),
    (35.6762, 139.6503, 200),
]

points: list[list[float]] = []
for lat, lng, n in BASE_CLUSTERS:
    for _ in range(n):
        points.append(
            [
                lat + random.gauss(0, 0.03),
                lng + random.gauss(0, 0.03),
                random.uniform(0.3, 1.0),
            ]
        )

m = folium.Map(location=[48.0, 10.0], zoom_start=3)
folium.plugins.HeatMap(
    points,
    min_opacity=min_opacity,
    radius=radius,
    blur=blur,
).add_to(m)

st_folium_vnext(m, key="heat-map", height=550)

with st.expander("Show code"):
    st.code(
        """\
import folium
import folium.plugins
import streamlit as st
from streamlit_folium_vnext import st_folium_vnext

# points = [[lat, lng, intensity], ...]
m = folium.Map(location=[48.0, 10.0], zoom_start=3)
folium.plugins.HeatMap(points, radius=20, blur=15, min_opacity=0.4).add_to(m)

st_folium_vnext(m, key="heat-map", height=550)
""",
        language="python",
    )
