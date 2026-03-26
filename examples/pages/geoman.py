import folium
import folium.elements
import streamlit as st
from jinja2 import Template

from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("Geoman Drawing Plugin")
st.write(
    "Draw shapes on the map using the Geoman toolbar. "
    "Supports drawing, editing, dragging, cutting, and rotating shapes."
)

# Create a MacroElement to load Geoman and initialize its controls
geoman = folium.MacroElement()
geoman._template = Template(
    """
    {% macro script(this, kwargs) %}
    {{ this._parent.get_name() }}.pm.addControls({
        position: 'topleft',
        drawCircle: true,
        drawCircleMarker: true,
        drawPolyline: true,
        drawRectangle: true,
        drawPolygon: true,
        drawMarker: true,
        drawText: true,
        editMode: true,
        dragMode: true,
        cutPolygon: true,
        removalMode: true,
        rotateMode: true,
    });
    {% endmacro %}
"""
)
geoman.default_js = [
    (
        "leaflet-geoman",
        "https://unpkg.com/@geoman-io/leaflet-geoman-free@2.17.0/dist/leaflet-geoman.min.js",
    ),
]
geoman.default_css = [
    (
        "leaflet-geoman-css",
        "https://unpkg.com/@geoman-io/leaflet-geoman-free@2.17.0/dist/leaflet-geoman.css",
    ),
]

m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
geoman.add_to(m)

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
