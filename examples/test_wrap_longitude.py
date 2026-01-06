"""
Test script to demonstrate the wrap_longitude parameter.

Pan the map around the world (past the dateline) and observe how
the longitude values change with wrap_longitude enabled vs disabled.
"""

import folium
import streamlit as st

from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("Test: wrap_longitude parameter")

st.markdown("""
**Instructions:** Pan the map to the left or right past the international dateline
(keep going past 180° or -180°). Watch how the center longitude and bounds change.

- **Without wrapping:** Longitude values can exceed -180/180 (e.g., -200, 250)
- **With wrapping:** Longitude values stay within -180 to 180
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("wrap_longitude=False (default)")
    m1 = folium.Map(location=[0, 170], zoom_start=2)
    result1 = st_folium(m1, key="map1", wrap_longitude=False, height=400, use_container_width=True)

    if result1:
        st.write("**Center:**", result1.get("center"))
        bounds1 = result1.get("bounds")
        if bounds1:
            sw = bounds1.get("_southWest", {})
            ne = bounds1.get("_northEast", {})
            st.write(f"**SW lng:** {sw.get('lng')}")
            st.write(f"**NE lng:** {ne.get('lng')}")

with col2:
    st.subheader("wrap_longitude=True")
    m2 = folium.Map(location=[0, 170], zoom_start=2)
    result2 = st_folium(m2, key="map2", wrap_longitude=True, height=400, use_container_width=True)

    if result2:
        st.write("**Center:**", result2.get("center"))
        bounds2 = result2.get("bounds")
        if bounds2:
            sw = bounds2.get("_southWest", {})
            ne = bounds2.get("_northEast", {})
            st.write(f"**SW lng:** {sw.get('lng')}")
            st.write(f"**NE lng:** {ne.get('lng')}")
