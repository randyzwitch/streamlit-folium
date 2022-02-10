import os
import re

import folium
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from folium.utilities import get_bounds, normalize
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


def st_folium(
    fig: folium.MacroElement, key: str = None, height: int = 500, width: int = 500
):
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
    map_leaflet = generate_leaflet_string(fig, nested=False)
    leaflet_without_map = leaflet.replace(map_leaflet, "")

    top_id = get_full_id(fig)

    leaflet = leaflet.replace(top_id, "map_div")

    # TODO: Handle a generic Figure

    map_details = {
        "center": fig.location,
        # "crs": f"L.CRS.{fig.crs}",
        "crs": f"{fig.crs}",
    }
    map_details.update(fig.options)

    st.expander("Show running code:").code(leaflet)
    st.expander("Show running code:").code(leaflet_without_map)

    component_value = _component_func(
        fig=leaflet,
        id=top_id,
        key=key,
        # default={"bbox": [0.01, 0.01]},
        height=height,
        width=width,
        map_details=map_details,
    )

    return component_value


def get_full_id(m: folium.MacroElement) -> str:
    return f"{m._name.lower()}_{m._id}"


def generate_leaflet_string(m: folium.MacroElement, nested: bool = True) -> str:
    leaflet: str = normalize(m._template.module.script(m))

    if not nested:
        return leaflet

    for _, child in m._children.items():
        try:
            leaflet += "\n" + generate_leaflet_string(child)
        except UndefinedError:
            pass

    return leaflet


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

    retdata = st_folium(m, key="blah")

    st.write(retdata)
