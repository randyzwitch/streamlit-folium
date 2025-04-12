import folium
import streamlit as st
from folium.plugins import Timeline, TimelineSlider
import requests

from streamlit_folium import st_folium

st.set_page_config(
    layout="wide"
)

m = folium.Map()

data = requests.get(
    "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
).json()

timeline = Timeline(
    data,
    get_interval=folium.JsCode(
        """
        function (quake) {
           // earthquake data only has a time, so we\'ll use that as a "start"
           // and the "end" will be that + some value based on magnitude
           // 18000000 = 30 minutes, so a quake of magnitude 5 would show on the
           // map for 150 minutes or 2.5 hours
           return {
               start: quake.properties.time,
               end: quake.properties.time + quake.properties.mag * 1800000,
           }
        }
    """
    ),
).add_to(m)
TimelineSlider(
    auto_play=False,
    show_ticks=True,
    enable_keyboard_controls=True,
    playback_duration=30000,
).add_timelines(timeline).add_to(m)

st_folium(m, debug=True, width=1200, height=500)
