import streamlit as st
import streamlit_folium

st.set_page_config(page_title="streamlit-folium documentation")

st.sidebar.write("# streamlit-folium")

st.sidebar.write("""
Display [folium](https://python-visualization.github.io/folium/) maps in [Streamlit](https://streamlit.io/), additionally returning data such as the bounding box to Streamlit for full geospatial interactivity! 
""")

st.sidebar.write("---")
f = st.sidebar.radio("Choose one of the examples below to see how to use the streamlit-folium library", ["st_folium", "folium_static"])


if f == "folium_static":

    streamlit_folium.folium_static

    "---"

    "### Examples:"
    with st.echo():

        import streamlit as st
        from streamlit_folium import folium_static
        import folium
        import branca

        page = st.radio(
            "Select map type", ["Single map", "Dual map", "Branca figure"], index=0
        )

        # center on Liberty Bell, add marker
        if page == "Single map":
            m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
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
        folium_static(m)
