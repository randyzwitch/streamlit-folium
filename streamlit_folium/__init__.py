import hashlib
import os
import re
from typing import Dict, List

import branca
import folium
import folium.plugins
import streamlit.components.v1 as components
from jinja2 import UndefinedError


def generate_js_hash(js_string: str, key: str = None) -> str:
    """
    Generate a standard key from a javascript string representing a series
    of folium-generated leaflet objects by replacing the hash's at the end
    of variable names (e.g. "marker_5f9d46..." -> "marker"), and returning
    the hash.
    """
    pattern = r"(_[a-z0-9]+)"
    standardized_js = re.sub(pattern, "", js_string) + str(key)
    s = hashlib.sha256(standardized_js.encode()).hexdigest()
    return s


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

    # if DualMap, get HTML representation
    elif isinstance(fig, folium.plugins.DualMap) or isinstance(
        fig, branca.element.Figure
    ):
        return components.html(fig._repr_html_(), height=height + 10, width=width)


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "st_folium", url="http://localhost:3001"
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_folium", path=build_dir)


def st_folium(
    fig: folium.MacroElement, key: str = None, height: int = 700, width: int = 500
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

    # handle the case where you pass in a figure rather than a map
    # this assumes that a map is the first child
    fig.render()

    if not (isinstance(fig, folium.Map) or isinstance(fig, folium.plugins.DualMap)):
        fig = list(fig._children.values())[0]

    leaflet = generate_leaflet_string(fig)

    # Replace the folium generated map_{random characters} variables
    # with map_div and map_div2 (these end up being both the assumed)
    # div id where the maps are inserted into the DOM, and the names of
    # the variables themselves.
    if isinstance(fig, folium.plugins.DualMap):
        m_id = m1_id = get_full_id(fig.m1)
        leaflet = leaflet.replace(m1_id, "map_div")
        m2_id = get_full_id(fig.m2)
        leaflet = leaflet.replace(m2_id, "map_div2")
    else:
        m_id = get_full_id(fig)
        leaflet = leaflet.replace(m_id, "map_div")

    # Get rid of the annoying popup
    leaflet = leaflet.replace("alert(coords);", "")

    if "drawnItems" not in leaflet:
        leaflet += "\nvar drawnItems = [];"

    def bounds_to_dict(bounds_list: List[List[float]]) -> Dict[str, Dict[str, float]]:
        southwest, northeast = bounds_list
        return {
            "_southWest": {
                "lat": southwest[0],
                "lng": southwest[1],
            },
            "_northEast": {
                "lat": northeast[0],
                "lng": northeast[1],
            },
        }

    component_value = _component_func(
        fig=leaflet,
        id=m_id,
        key=generate_js_hash(leaflet, key),
        height=height,
        width=width,
        default={
            "last_clicked": None,
            "last_object_clicked": None,
            "all_drawings": None,
            "last_active_drawing": None,
            "bounds": bounds_to_dict(fig.get_bounds()),
            "zoom": fig.options.get("zoom") if hasattr(fig, "options") else {},
            "last_circle_radius": None,
            "last_circle_polygon": None,
        },
    )

    return component_value


def get_full_id(m: folium.MacroElement) -> str:
    if isinstance(m, folium.plugins.DualMap):
        m = m.m1
    return f"{m._name.lower()}_{m._id}"


def generate_leaflet_string(m: folium.MacroElement, nested: bool = True) -> str:
    if isinstance(m, folium.plugins.DualMap):
        if not nested:
            return generate_leaflet_string(m.m1, nested=False)
        # Generate the script for map1
        leaflet = generate_leaflet_string(m.m1, nested=nested)
        # Add the script for map2
        leaflet += "\n" + generate_leaflet_string(m.m2, nested=nested)
        # Add the script that syncs them together
        leaflet += m._template.module.script(m)
        return leaflet

    try:
        leaflet = m._template.module.script(m)
    except UndefinedError:
        # Correctly render Popup elements, and perhaps others. Not sure why
        # this is necessary. Some deep magic related to jinja2 templating, perhaps.
        leaflet = m._template.render(this=m, kwargs={})

    if not nested:
        return leaflet

    for _, child in m._children.items():
        try:
            leaflet += "\n" + generate_leaflet_string(child)
        except UndefinedError:
            pass

    return leaflet
