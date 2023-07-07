import folium
import streamlit as st
from folium.features import Marker, Popup

from streamlit_folium import st_folium

st.write("# Simple Popup & Tooltip")

return_on_hover = st.checkbox("Return on hover?")

with st.echo("below"):
    m = folium.Map(location=[45, -122], zoom_start=4)

    Marker(
        location=[45.5, -122],
        popup=Popup("Popup!", parse_html=False),
        tooltip="Tooltip!",
    ).add_to(m)

    Marker(
        location=[45.5, -112],
        popup=Popup("Popup 2!", parse_html=False),
        tooltip="Tooltip 2!",
    ).add_to(m)

    out = st_folium(m, height=200, return_on_hover=return_on_hover)

    st.write("Popup:", out["last_object_clicked_popup"])
    st.write("Tooltip:", out["last_object_clicked_tooltip"])
