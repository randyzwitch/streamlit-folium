import folium
import requests
import streamlit as st
from folium.plugins.pattern import CirclePattern, StripePattern

from streamlit_folium import st_folium

st.write("# GeoJson Fill Patterns")
st.write(
    "A GeoJson layer can be filled with a repeating pattern instead of a flat "
    "color, by putting a `StripePattern` or `CirclePattern` into the "
    "`fillPattern` field returned by a style function. The pattern has to be "
    "added to the map as well, so it exists for the style to point at."
)
st.write(
    "See [original](https://python-visualization.github.io/folium/latest/user_guide/plugins/pattern.html)"
)


@st.cache_resource
def get_states() -> dict:
    response = requests.get(
        "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json"
    )
    return response.json()


m = folium.Map(location=[39.5, -110.0], zoom_start=5)

stripes = StripePattern(angle=-45).add_to(m)
circles = CirclePattern(
    width=20, height=20, radius=5, fill_opacity=0.5, opacity=1
).add_to(m)

patterned = {"Colorado": stripes, "Utah": circles}


def style_function(feature):
    style = {
        "opacity": 1.0,
        "fillColor": "#ffff00",
        "color": "black",
        "weight": 2,
    }
    pattern = patterned.get(feature["properties"]["name"])
    if pattern is not None:
        style["fillPattern"] = pattern
        style["fillOpacity"] = 1.0
    return style


folium.GeoJson(
    get_states(),
    smooth_factor=0.5,
    style_function=style_function,
).add_to(m)

st_folium(m, width=800, height=450)
