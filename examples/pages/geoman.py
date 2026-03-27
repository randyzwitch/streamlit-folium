import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: Geoman Drawing Plugin",
    page_icon=":pencil2:",
    layout="wide",
)

"""
# streamlit-folium: Geoman Drawing Plugin

[Leaflet-Geoman](https://geoman.io/) is a modern alternative to Leaflet.Draw,
with support for drawing, editing, dragging, cutting, and rotating shapes.

Since Geoman is a Leaflet plugin, you can add it to your folium map using a
`MacroElement` that loads the Geoman JS/CSS and initializes its controls.
streamlit-folium automatically detects Geoman and returns drawing data via the
`geoman_drawings` and `last_geoman_drawing` data fields.

Draw something below to see the return value back to Streamlit!
"""

with st.echo(code_location="below"):
    import folium
    import folium.elements
    import streamlit as st
    from jinja2 import Template

    from streamlit_folium import st_folium

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

    c1, c2 = st.columns(2)
    with c1:
        output = st_folium(m, width=700, height=500)

    with c2:
        st.write(output)
