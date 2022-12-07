import branca
import folium
import folium.plugins
import streamlit as st

from streamlit_folium import st_folium

page = st.radio("Select map type", ["Single map", "Dual map", "Branca figure"], index=0)

# center on Liberty Bell, add marker
if page == "Single map":
    with st.echo():
        m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
        tooltip = "Liberty Bell"
        legend_img = "https://placekitten.com/200/300"
        url = "https://raw.githubusercontent.com/SECOORA/static_assets/master/maps/img/rose.png"
        szt = folium.plugins.FloatImage(url, bottom=60, left=70, width="20%")
        m.add_child(szt)
        folium.Marker(
            [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
        ).add_to(m)

elif page == "Dual map":
    with st.echo():
        m = folium.plugins.DualMap(location=[39.949610, -75.150282], zoom_start=16)
        tooltip = "Liberty Bell"
        folium.Marker(
            [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
        ).add_to(m)

else:
    with st.echo():
        m = branca.element.Figure()
        fm = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
        tooltip = "Liberty Bell"
        folium.Marker(
            [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
        ).add_to(fm)
        m.add_child(fm)

with st.echo():
    # call to render Folium map in Streamlit
    st_folium(m, width=2000, height=500, returned_objects=[])
