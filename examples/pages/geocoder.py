import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: Geocoder",
    page_icon=":mag:",
    layout="wide",
)

"""
# streamlit-folium: Geocoder Plugin

Folium supports the
[`Geocoder`](https://python-visualization.github.io/folium/plugins.html#folium.plugins.Geocoder)
plugin, which adds a search box to the map powered by
[leaflet-control-geocoder](https://github.com/perliedman/leaflet-control-geocoder).

When a search result is selected, the place name, coordinates, bounding box, and
properties are passed back via the `last_geocoder_result` data field.

Search for a place below to see the return value back to Streamlit!
"""

with st.echo(code_location="below"):
    import folium
    import streamlit as st
    from folium.plugins import Geocoder

    from streamlit_folium import st_folium

    m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
    Geocoder().add_to(m)

    c1, c2 = st.columns(2)
    with c1:
        output = st_folium(m, width=700, height=500)

    with c2:
        st.write(output)
