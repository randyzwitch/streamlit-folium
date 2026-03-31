import folium
import streamlit as st

from streamlit_folium import st_folium

START_LOCATION = [37.7934347109497, -122.399077892527]
START_ZOOM = 17

if "map_center" not in st.session_state:
    st.session_state["map_center"] = START_LOCATION
if "map_zoom" not in st.session_state:
    st.session_state["map_zoom"] = START_ZOOM


def move_map(coord, zoom):
    st.session_state["map_center"] = coord
    st.session_state["map_zoom"] = zoom


coord1 = [37.7934347109497, -122.399077892527]
zoom1 = 17.01
marker1 = folium.Marker(location=coord1)

coord2 = [37.7937070646238, -122.43]
zoom2 = 17.02
marker2 = folium.Marker(location=coord2)

st.button(
    "go to marker right",
    on_click=move_map,
    args=(
        coord1,
        zoom1,
    ),
)
st.button(
    "go to marker left",
    on_click=move_map,
    args=(
        coord2,
        zoom2,
    ),
)

map = folium.Map(
    location=START_LOCATION, zoom_start=START_ZOOM, tiles="OpenStreetMap", max_zoom=21
)
marker1.add_to(map)
marker2.add_to(map)

st_folium(
    map,
    width=800,
    center=st.session_state["map_center"],
    zoom=st.session_state["map_zoom"],
    height=450,
    debug=True,
)
