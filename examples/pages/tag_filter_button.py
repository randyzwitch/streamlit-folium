import streamlit as st

st.set_page_config(
    page_title="streamlit-folium documentation: TagFilterButton",
    page_icon=":label:",
    layout="wide",
)

"""
# streamlit-folium: TagFilterButton

Folium supports the
[`TagFilterButton`](https://python-visualization.github.io/folium/plugins.html#folium.plugins.TagFilterButton)
plugin, which allows filtering markers on the map by tags.

When tags are selected or deselected, the currently active tags are passed back
via the `selected_tags` data field.

Click the filter button (funnel icon) on the map to select tags and see the
return value back to Streamlit!
"""

with st.echo(code_location="below"):
    import folium
    import streamlit as st
    from folium.plugins import TagFilterButton

    from streamlit_folium import st_folium

    m = folium.Map(location=[45.5, -122.6], zoom_start=12)

    folium.Marker(
        [45.5, -122.6], tooltip="Restaurant A", tags=["restaurant", "downtown"]
    ).add_to(m)
    folium.Marker(
        [45.52, -122.62], tooltip="Park B", tags=["park", "downtown"]
    ).add_to(m)
    folium.Marker(
        [45.48, -122.58], tooltip="Restaurant C", tags=["restaurant", "eastside"]
    ).add_to(m)
    folium.Marker(
        [45.51, -122.65], tooltip="Park D", tags=["park", "westside"]
    ).add_to(m)

    TagFilterButton(
        ["restaurant", "park", "downtown", "eastside", "westside"]
    ).add_to(m)

    c1, c2 = st.columns(2)
    with c1:
        output = st_folium(m, width=700, height=500)

    with c2:
        st.write(output)
