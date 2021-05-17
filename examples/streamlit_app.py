import streamlit as st

st.set_page_config(page_title="streamlit-folium documentation")

"# streamlit-folium"

with st.echo():

    import streamlit as st
    from streamlit_folium import folium_static
    import folium

    page = st.radio("Select map type", ["Single map", "Dual map"], index=0)

    # center on Liberty Bell
    if page == "Single map":
        m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
    elif page == "Dual map":
        m = folium.plugins.DualMap(location=[39.949610, -75.150282], zoom_start=16)

    # add marker for Liberty Bell
    tooltip = "Liberty Bell"
    folium.Marker(
        [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
    ).add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)
