import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: LocateControl",
    page_icon=":round_pushpin:",
    layout="wide",
)

"""
# streamlit-folium: LocateControl Plugin

Folium supports the
[`LocateControl`](https://python-visualization.github.io/folium/latest/user_guide/plugins/locate_control.html)
plugin, which adds a button to the map that shows the user's current position using
[leaflet-locatecontrol](https://github.com/domoritz/leaflet-locatecontrol).

When the browser finds the user's location, the latitude, longitude, and accuracy
(in meters) are passed back via the `last_located` data field. To avoid rerunning
the app on GPS noise, `last_located` only updates once the user has moved a
meaningful distance (at least 10 m, or more when the location fix is less accurate).
Note that `last_located` is filled by any call to `map.locate()` on the map, not
only by `LocateControl`.

Click the location button on the map (and allow location access in your browser) to
see the return value back to Streamlit!
"""

with st.echo(code_location="below"):
    import folium
    import streamlit as st
    from folium.plugins import LocateControl

    from streamlit_folium import st_folium

    m = folium.Map(location=[39.949610, -75.150282], zoom_start=4)
    LocateControl(setView="once").add_to(m)

    c1, c2 = st.columns(2)
    with c1:
        output = st_folium(m, width=700, height=500, returned_objects=["last_located"])

    with c2:
        st.write(output)
