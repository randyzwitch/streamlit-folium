import folium
import streamlit as st

from streamlit_folium import st_folium

st.set_page_config(layout="wide")

m = folium.Map(location=(45, -90), zoom_start=5)

left, right = st.columns([2, 1])
with left:
    st_folium(m, use_container_width=True, key="1")
with right:
    st_folium(m, use_container_width=True, key="2")

st_folium(m, use_container_width=True, key="3")


col1, col2, col3 = st.columns([1, 2, 3])

with col1:
    st_folium(m, use_container_width=True, key="4")
with col2:
    st_folium(m, use_container_width=True, key="5")
with col3:
    st_folium(m, use_container_width=True, key="6")
