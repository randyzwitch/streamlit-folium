import folium
import streamlit as st

from streamlit_folium import st_folium

st.set_page_config(
    layout="wide",
    page_title="streamlit-folium documentation: Fit Bounds",
    page_icon="random",
)
"""
# streamlit-folium: Fit Bounds

Use `map.fit_bounds()` to automatically zoom and center the map to fit a
specified bounding box. This is useful when you want to ensure all your
data is visible on the map.
"""

# Define bounds: Southwest and Northeast corners
# This covers the Pacific Northwest region of North America
bounds = [[40.0, -125.0], [50.0, -115.0]]

st.subheader("Using map.fit_bounds()")

st.markdown("""
The `fit_bounds()` method adjusts the map view to contain the given
geographical bounds with the maximum zoom level possible.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### With fit_bounds")
    m1 = folium.Map(location=[0, 0], zoom_start=2, tiles="cartodbpositron")
    m1.fit_bounds(bounds)

    # Add a rectangle to visualize the bounds
    folium.Rectangle(
        bounds=bounds,
        color="red",
        weight=2,
        fill=True,
        fill_opacity=0.1,
    ).add_to(m1)

    st_folium(m1, use_container_width=True, height=400, key="with_fit_bounds")

with col2:
    st.markdown("### Without fit_bounds")
    m2 = folium.Map(location=[0, 0], zoom_start=2, tiles="cartodbpositron")

    # Add the same rectangle for comparison
    folium.Rectangle(
        bounds=bounds,
        color="blue",
        weight=2,
        fill=True,
        fill_opacity=0.1,
    ).add_to(m2)

    st_folium(m2, use_container_width=True, height=400, key="without_fit_bounds")

st.divider()

st.subheader("fit_bounds with padding")

st.markdown("""
You can add padding around the bounds to give some extra space:
- `padding`: Equal padding on all sides
- `padding_top_left`: Padding for top-left corner
- `padding_bottom_right`: Padding for bottom-right corner
""")

m3 = folium.Map(tiles="cartodbpositron")
m3.fit_bounds(bounds, padding=(50, 50))

folium.Rectangle(
    bounds=bounds,
    color="green",
    weight=2,
    fill=True,
    fill_opacity=0.1,
    popup="Bounds with padding=(50, 50)",
).add_to(m3)

st_folium(m3, use_container_width=True, height=400, key="with_padding")

st.divider()

st.subheader("Code Example")

st.code(
    """
import folium
from streamlit_folium import st_folium

# Define bounds as [[south, west], [north, east]]
bounds = [[40.0, -125.0], [50.0, -115.0]]

# Create map and fit to bounds
m = folium.Map()
m.fit_bounds(bounds)

# Optionally add padding
# m.fit_bounds(bounds, padding=(50, 50))

st_folium(m, use_container_width=True)
""",
    language="python",
)
