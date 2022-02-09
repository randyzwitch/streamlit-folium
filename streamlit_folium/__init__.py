import os
from typing import Dict

import folium
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from jinja2 import UndefinedError


def folium_static(fig, width=700, height=500):

    """
    Renders `folium.Figure` or `folium.Map` in a Streamlit app. This method is
    a static Streamlit Component, meaning, no information is passed back from
    Leaflet on browser interaction.
    Parameters
    ----------
    fig  : folium.Map or folium.Figure
        Geospatial visualization to render
    width : int
        Width of result
    Height : int
        Height of result
    Note
    ----
    If `height` is set on a `folium.Map` or `folium.Figure` object,
    that value supersedes the values set with the keyword arguments of this function.
    Example
    -------
    >>> m = folium.Map(location=[45.5236, -122.6750])
    >>> folium_static(m)
    """

    # if Map, wrap in Figure
    if isinstance(fig, folium.Map):
        fig = folium.Figure().add_child(fig)

    return components.html(
        fig.render(), height=(fig.height or height) + 10, width=width
    )


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "st_folium", url="http://localhost:3001"
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_folium", path=build_dir)


def st_folium(fig, key=None):
    """Display a Folium object in Streamlit, returning data as user interacts
    with app.
    Parameters
    ----------
    fig  : folium.Map or folium.Figure
        Geospatial visualization to render
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    Returns
    -------
    dict
        Selected data from Folium/leaflet.js interactions in browser
    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.

    # parse out folium figure html from Jupyter representation
    # since this contains everything needed to build chart
    # soup = BeautifulSoup(fig._repr_html_(), "html.parser")

    # base64 representation of the data inside the iframe
    # represents most if not all code needed to build map
    # data_html = soup.iframe["data-html"]

    # TODO: think about data to pass to React. It's not the value of "fig"
    # data_html currently there since str can be mapped to JSON
    leaflet = generate_leaflet_string(fig)
    top_id = get_full_id(fig)

    st.expander("Show running code:").code(leaflet)

    component_value = _component_func(
        fig=leaflet, id=top_id, key=key, default={"bbox": [0.01, 0.01]}, height=500
    )

    return component_value


def get_full_id(m: folium.MacroElement) -> str:
    return f"{m._name.lower()}_{m._id}"


def generate_leaflet_string(m: folium.MacroElement) -> str:
    leaflet: str = m._template.module.script(m)

    for _, child in m._children.items():
        try:
            leaflet += "\n" + generate_leaflet_string(child)
        except UndefinedError:
            pass

    return leaflet


def map_to_dict(m: folium.Map) -> Dict:
    name = m._name
    location = m.location
    crs = m.crs
    options = m.options
    m._template

    for child in m._children:
        child._name

    return {}


x = """
{
  "_name": "Map",
  "_id": "2a49529b79ec42a89c5739373d3d7c86",
  "_env": "<jinja2.environment.Environment object at 0x12d454af0>",
  "_children": {
    "stamenterrain": "<folium.raster_layers.TileLayer object at 0x12d7fe7f0>",
    "marker_88cdf44f57a2408ab5966f3c96fb4757": "<folium.map.Marker object at 0x12cddf9d0>",
    "marker_a02bba96eb864e8fae49a4e440e650db": "<folium.map.Marker object at 0x12d7fefd0>"
  },
  "_parent": "<branca.element.Figure object at 0x12d728460>",
  "_png_image": null,
  "png_enabled": false,
  "location": [
    45.372,
    -121.6972
  ],
  "width": [
    100,
    "%"
  ],
  "height": [
    100,
    "%"
  ],
  "left": [
    0,
    "%"
  ],
  "top": [
    0,
    "%"
  ],
  "position": "relative",
  "crs": "EPSG3857",
  "control_scale": false,
  "options": {
    "zoom": 12,
    "zoomControl": true,
    "preferCanvas": false
  },
  "global_switches": "<folium.folium.GlobalSwitches object at 0x12d7fef40>",
  "objects_to_stay_in_front": []
}
"""

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    from streamlit_folium import folium_static

    m = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles="Stamen Terrain")
    tooltip = "Click me!"
    folium.Marker(
        [45.3288, -121.6625], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
    ).add_to(m)
    folium.Marker(
        [45.3311, -121.7113], popup="<b>Timberline Lodge</b>", tooltip=tooltip
    ).add_to(m)

    # fig = folium.Figure().add_child(m)

    _ = """
    st.write(m.to_json())
    st.write(m.to_dict())

    for _, c in m._children.items():
        st.write("RENDERED")
        st.write(str(c._template.render()))

    components.html(fig._repr_html_(), height=500 + 10, width=700)
    """

    # parse out object, pull data-html value from it
    # surrounding divs and iframes prob not
    # soup = BeautifulSoup(m._repr_html_(), "html.parser")
    # st.write(soup.iframe["data-html"])
    # st.write(vars(m))
    # st.write("Children:")
    # for key, child in m._children.items():
    #    st.write(key)
    #    st.write(vars(child))
    # st.write(vars(m._env))
    # data_html = soup.iframe["data-html"]

    # ideally, this should return a Dict with expected keys
    retdata = st_folium(m)

    # retdata

    # print(m._repr_html_())
