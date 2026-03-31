from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="vnext multipage demo", layout="wide")
st.title("streamlit-folium vnext")
st.markdown(
    """
    Multipage demo for testing the `streamlit_folium_vnext` component.

    **Pages:**
    - **Basic Map** — Markers, panning, zoom. Verify no flicker on interaction.
    - **Click Events** — Click the map, see lat/lng update in real time.
    - **Drawing** — Draw shapes using Leaflet.Draw, see GeoJSON output.
    - **GeoJSON** — Load various GeoJSON features onto a map.
    - **Multiple Maps** — Two independent maps side by side.
    """
)
