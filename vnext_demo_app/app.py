from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="streamlit-folium vnext", layout="wide", page_icon=":material/map:"
)

pg = st.navigation(
    {
        "Core": [
            st.Page("pages/basic_map.py", title="Basic Map", icon=":material/map:"),
            st.Page(
                "pages/click_events.py",
                title="Click Events",
                icon=":material/ads_click:",
            ),
        ],
        "Features": [
            st.Page("pages/drawing.py", title="Drawing", icon=":material/draw:"),
            st.Page("pages/geojson.py", title="GeoJSON", icon=":material/layers:"),
            st.Page(
                "pages/multiple_maps.py",
                title="Multiple Maps",
                icon=":material/grid_view:",
            ),
        ],
        "Advanced": [
            st.Page(
                "pages/accumulated_state.py",
                title="Accumulated State",
                icon=":material/history:",
            ),
            st.Page(
                "pages/dynamic_map.py",
                title="Dynamic Map",
                icon=":material/add_location:",
            ),
        ],
    }
)
pg.run()
