"""
Template file for creating a streamlit-folium example
that can be integrated with the st.navigation system.

This file is designed to be used in two ways:
1. Added to the examples/pages/ directory for discovery by streamlit_app.py
2. Referenced by st.Page() in streamlit_app.py to be included in navigation

For more information on Material Design icons for use in navigation, see:
https://fonts.google.com/icons
"""

import folium
import streamlit as st

from streamlit_folium import st_folium

# Page content
st.title("Example Template")

st.markdown("""
This is a template file showing how to structure a streamlit-folium example
that works with Streamlit's navigation system.

Replace this text with your own description.
""")

# Simple map example
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

# Display the map
st_data = st_folium(m, width=725)

# Show returned data
st.write("Map data:", st_data)
