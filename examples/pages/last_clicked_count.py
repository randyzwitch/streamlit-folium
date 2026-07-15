import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: Last Clicked Count",
    page_icon="🔢",
    layout="wide",
)

"""
# streamlit-folium: Last Clicked Count

`last_object_clicked_count` increments every time a marker or drawing is clicked,
so app code can detect repeated clicks on the same object even when the lat/lng
has not changed.
"""

with st.echo(code_location="below"):
    import folium
    import streamlit as st

    from streamlit_folium import st_folium

    m = folium.Map(location=[39.949610, -75.150282], zoom_start=13)

    folium.Marker(
        [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
    ).add_to(m)

    output = st_folium(
        m,
        width=700,
        height=500,
        returned_objects=["last_object_clicked", "last_object_clicked_count"],
    )

    st.write(output)
    st.write(f"Click count: {output.get('last_object_clicked_count')}")
