import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: Static Map",
    page_icon=":ice:",
)

"""
# streamlit-folium: Non-interactive Map

If you don't need any data returned from the map, you can just use the folium_static
function to simply embed a map in your Streamlit app. The streamlit app will not rerun
when the user interacts with the map, and you will not get any data back from the map.

Behind the scenes, this is just a wrapper around `st_folium` that sets
`returned_objects=[]`

---

"""
"### Basic `folium_static()` Example"

with st.echo():

    import folium
    import streamlit as st

    from streamlit_folium import folium_static

    # center on Liberty Bell, add marker
    m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
    folium.Marker(
        [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
    ).add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m, width=725)
