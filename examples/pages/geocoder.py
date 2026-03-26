import folium
from folium.plugins import Geocoder

import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("Geocoder Plugin Example")
st.write("Search for a place using the search box on the map.")

m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
Geocoder().add_to(m)

output = st_folium(m, width=700, height=500)

st.write("## Map Output")
if output and output.get("last_geocoder_result"):
    result = output["last_geocoder_result"]
    st.write(f"**Place:** {result.get('name')}")
    st.write(f"**Coordinates:** ({result.get('lat')}, {result.get('lng')})")
    if result.get("bbox"):
        st.write(f"**Bounding Box:** {result['bbox']}")
    if result.get("properties"):
        st.write("**Properties:**", result["properties"])

st.write("### Raw output")
st.write(output)
