import folium
import streamlit as st

from streamlit_folium import Geoman, st_folium

st.set_page_config(layout="wide")
st.title("Geoman Drawing Plugin")
st.write(
    "Draw shapes on the map using the Geoman toolbar. "
    "Supports drawing, editing, dragging, cutting, and rotating shapes."
)

m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
Geoman(
    position="topleft",
    draw_marker=True,
    draw_polygon=True,
    draw_polyline=True,
    draw_rectangle=True,
    draw_circle=True,
    edit_mode=True,
    drag_mode=True,
    cut_polygon=True,
    removal_mode=True,
    rotate_mode=True,
).add_to(m)

output = st_folium(m, width=700, height=500)

st.write("## Drawings")
if output and output.get("last_geoman_drawing"):
    st.write("### Last Drawing")
    st.json(output["last_geoman_drawing"])

if output and output.get("geoman_drawings"):
    st.write(f"### All Drawings ({len(output['geoman_drawings'])} total)")
    for i, drawing in enumerate(output["geoman_drawings"]):
        st.write(f"**Drawing {i + 1}:**")
        st.json(drawing)

st.write("### Raw output")
st.write(output)
