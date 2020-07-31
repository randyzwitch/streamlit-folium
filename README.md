# streamlit-folium

![Run tests each PR](https://github.com/randyzwitch/streamlit-folium/workflows/Run%20tests%20each%20PR/badge.svg)

This Streamlit Component is a work-in-progress to determine what functionality is desirable for a Folium and Streamlit integration. Currently, one method `folium_static()` is defined, which takes a `folium.Map` or `folium.Figure` object and displays it in a Streamlit app.

## Installation

```python
pip install streamlit-folium
```

## Example

```python
import streamlit as st
from streamlit_folium import folium_static
import folium

"# streamlit-folium"

with st.echo():
    import streamlit as st
    from streamlit_folium import folium_static
    import folium

    # center on Liberty Bell
    m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)

    # add marker for Liberty Bell
    tooltip = "Liberty Bell"
    folium.Marker(
        [39.949610, -75.150282], popup="Liberty Bell", tooltip=tooltip
    ).add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)
```

!["streamlit_folium example"](_static/streamlit_folium_example.png)
