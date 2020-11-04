import os
import streamlit.components.v1 as components
import folium


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
        "st_folium",
        url="http://localhost:3001",
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

    # TODO: think about data to pass to React. It's not the value of "fig"
    component_value = _component_func(
        fig=fig, key=key, default={"bbox": [0.01, 0.01], "no": False}
    )

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st
    from streamlit_folium import folium_static

    import folium
    from bs4 import BeautifulSoup

    m = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles="Stamen Terrain")
    tooltip = "Click me!"
    folium.Marker(
        [45.3288, -121.6625], popup="<i>Mt. Hood Meadows</i>", tooltip=tooltip
    ).add_to(m)
    folium.Marker(
        [45.3311, -121.7113], popup="<b>Timberline Lodge</b>", tooltip=tooltip
    ).add_to(m)

    # m.save("test.html")

    # fig = folium.Figure().add_child(m)

    # parse out object, pull data-html value from it
    # surrounding divs and iframes prob not
    soup = BeautifulSoup(m._repr_html_(), "html.parser")
    data_html = soup.iframe["data-html"]

    # ideally, this should return a Dict with expected keys
    retdata = st_folium(data_html)

    retdata
