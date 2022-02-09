import streamlit as st

st.set_page_config(page_title="streamlit-folium documentation")

"# streamlit-folium"

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
