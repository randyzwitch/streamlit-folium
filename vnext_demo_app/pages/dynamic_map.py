from __future__ import annotations

import random

import folium
import streamlit as st

from streamlit_folium_vnext import st_folium_vnext

st.title("Dynamic Map")
st.caption(
    "The map updates incrementally — adding a marker does not rebuild or flicker the map."
)

if "markers" not in st.session_state:
    st.session_state.markers = []

col_left, col_right = st.columns([2, 1])

with col_left:
    m = folium.Map(location=[20.0, 0.0], zoom_start=2)
    for _i, (lat, lng, label) in enumerate(st.session_state.markers):
        folium.Marker(
            [lat, lng],
            tooltip=label,
            popup=f"<b>{label}</b><br>{lat:.4f}, {lng:.4f}",
        ).add_to(m)

    result = st_folium_vnext(m, key="dynamic-map", height=500, subscribe=["click"])

    with st.expander("Show code"):
        st.code(
            """\
import random
import folium
import streamlit as st
from streamlit_folium_vnext import st_folium_vnext

if "markers" not in st.session_state:
    st.session_state.markers = []

m = folium.Map(location=[20.0, 0.0], zoom_start=2)
for _i, (lat, lng, label) in enumerate(st.session_state.markers):
    folium.Marker([lat, lng], tooltip=label).add_to(m)

result = st_folium_vnext(m, key="dynamic-map", height=500, subscribe=["click"])
# New markers appear instantly without map flicker — the JS layer
# cache diffs spec.layers by ID and adds only what changed.
""",
            language="python",
        )

with col_right:
    st.subheader("Markers")
    st.metric("Total", len(st.session_state.markers))

    if st.button("Add Random Marker", type="primary", use_container_width=True):
        lat = round(random.uniform(-55, 70), 4)
        lng = round(random.uniform(-170, 170), 4)
        n = len(st.session_state.markers) + 1
        st.session_state.markers.append((lat, lng, f"Marker {n}"))
        st.rerun()

    if st.button("Clear All", use_container_width=True):
        st.session_state.markers = []
        st.rerun()

    if st.session_state.markers:
        st.divider()
        for i, (lat, lng, label) in enumerate(st.session_state.markers):
            st.text(f"{i + 1}. {label}: ({lat}, {lng})")
    else:
        st.info("Click **Add Random Marker** to place markers on the map.")

    if result and result.event and result.event.get("type") == "click":
        payload = result.event["payload"]
        obj = payload.get("object")
        st.divider()
        if obj and obj.get("kind") == "marker":
            st.success(f"Clicked **{obj.get('tooltip', '?')}**")
        elif not obj:
            lat_c, lng_c = payload["lat"], payload["lng"]
            n = len(st.session_state.markers) + 1
            st.session_state.markers.append(
                (round(lat_c, 4), round(lng_c, 4), f"Marker {n}")
            )
            st.rerun()
