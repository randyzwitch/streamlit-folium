from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="streamlit-folium vnext", layout="wide", page_icon=":material/map:"
)

pg = st.navigation(
    {
        "Core": [
            st.Page(
                "vnext_demo_app/pages/basic_map.py",
                title="Basic Map",
                icon=":material/map:",
            ),
            st.Page(
                "vnext_demo_app/pages/click_events.py",
                title="Click Events",
                icon=":material/ads_click:",
            ),
        ],
        "Features": [
            st.Page(
                "vnext_demo_app/pages/drawing.py",
                title="Drawing",
                icon=":material/draw:",
            ),
            st.Page(
                "vnext_demo_app/pages/geojson.py",
                title="GeoJSON",
                icon=":material/layers:",
            ),
            st.Page(
                "vnext_demo_app/pages/vector_shapes.py",
                title="Vector Shapes",
                icon=":material/pentagon:",
            ),
            st.Page(
                "vnext_demo_app/pages/marker_cluster.py",
                title="Marker Cluster",
                icon=":material/bubble_chart:",
            ),
            st.Page(
                "vnext_demo_app/pages/heat_map.py",
                title="Heat Map",
                icon=":material/whatshot:",
            ),
            st.Page(
                "vnext_demo_app/pages/multiple_maps.py",
                title="Multiple Maps",
                icon=":material/grid_view:",
            ),
        ],
        "Advanced": [
            st.Page(
                "vnext_demo_app/pages/accumulated_state.py",
                title="Accumulated State",
                icon=":material/history:",
            ),
            st.Page(
                "vnext_demo_app/pages/dynamic_map.py",
                title="Dynamic Map",
                icon=":material/add_location:",
            ),
        ],
    }
)
pg.run()
