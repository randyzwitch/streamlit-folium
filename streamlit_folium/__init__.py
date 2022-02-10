import hashlib
import os
import re

import branca
import folium
import folium.plugins
import streamlit.components.v1 as components
from folium.utilities import normalize
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
    st.code(s)
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

    leaflet = generate_leaflet_string(fig)
    if isinstance(fig, folium.plugins.DualMap):
        m_id = m1_id = get_full_id(fig.m1)
        leaflet = leaflet.replace(m1_id, "map_div")
        m2_id = get_full_id(fig.m2)
        leaflet = leaflet.replace(m2_id, "map_div2")
    else:
        m_id = get_full_id(fig)
        leaflet = leaflet.replace(m_id, "map_div")

    # map_leaflet = generate_leaflet_string(fig, nested=False)
    # st.code(map_leaflet)
    # leaflet_without_map = leaflet.replace(map_leaflet, "")

    # TODO: Handle a generic Figure

    st.expander("Show running code:").code(leaflet)
    # st.expander("Show running code:").code(leaflet_without_map)

    component_value = _component_func(
        fig=leaflet,
        id=m_id,
        key=generate_js_hash(leaflet, key),
        height=height,
        width=width,
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
        leaflet += normalize(m._template.module.script(m))
        return leaflet

    leaflet = normalize(m._template.module.script(m))

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

    x = """
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

    import streamlit as st

    m = folium.Map(location=[45.5236, -122.6750], tiles="Stamen Toner", zoom_start=13)

    folium.Circle(
        radius=100,
        location=[45.5244, -122.6699],
        popup="The Waterfront",
        color="crimson",
        fill=False,
    ).add_to(m)

    folium.CircleMarker(
        location=[45.5215, -122.6261],
        radius=50,
        popup="Laurelhurst Park",
        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ).add_to(m)

    retdata = st_folium(m, key="blah")

    st.write(retdata)
    """

    # from streamlit_folium import folium_static

    page = st.radio(
        "Select map type",
        ["Single map", "Dual map", "Branca figure"],
        index=1,
        key="blah",
    )

    zoom = st.slider("Zoom", 1, 20, 16)
    # center on Liberty Bell, add marker
    if page == "Single map":
        m = folium.Map(location=[39.949610, -75.150282], zoom_start=zoom)
        tooltip = "Liberty Bell"
        folium.Marker(
            [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
        ).add_to(m)

    elif page == "Dual map":
        m = folium.plugins.DualMap(location=[39.949610, -75.150282], zoom_start=16)
        tooltip = "Liberty Bell"
        folium.Marker(
            [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
        ).add_to(m)

    elif page == "Branca figure":
        m = branca.element.Figure()
        fm = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
        tooltip = "Liberty Bell"
        folium.Marker(
            [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
        ).add_to(fm)
        m.add_child(fm)

    # call to render Folium map in Streamlit
    # folium_static(m)
    retdata = st_folium(m, key="fig1")
    st.write(retdata)

    # retdata = st_folium(m, key="fig2")
    # st.write(retdata)

    x = """
    url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
    antarctic_ice_edge = f"{url}/antarctic_ice_edge.json"
    antarctic_ice_shelf_topo = f"{url}/antarctic_ice_shelf_topo.json"

    m = folium.Map(
        location=[-59.1759, -11.6016],
        tiles="cartodbpositron",
        zoom_start=2,
    )

    folium.GeoJson(antarctic_ice_edge, name="geojson").add_to(m)

    folium.TopoJson(
        json.loads(requests.get(antarctic_ice_shelf_topo).text),
        "objects.antarctic_ice_shelf",
        name="topojson",
    ).add_to(m)

    folium.LayerControl().add_to(m)

    retdata2 = st_folium(m, key="blah2")

    st.write(retdata2)
    """
