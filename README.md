# streamlit-folium: geospatial made easy in Streamlit!


![Run tests each PR](https://github.com/randyzwitch/streamlit-folium/workflows/Run%20tests%20each%20PR/badge.svg)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/randyzwitch/streamlit-folium/examples/streamlit_app.py)

streamlit-folium integrates two great open-source projects in the Python ecosystem: [Streamlit](https://streamlit.io/) and [Folium](https://python-visualization.github.io/folium/)!

## Installation

```python
pip install streamlit-folium

or

conda install -c conda-forge streamlit-folium
```

## Usage

Currently, there are two functions defined:

- `st_folium()`: a bi-directional Component, taking a Folium/Branca object and plotting to the Streamlit app. Upon mount/interaction with the Streamlit app, `st_folium()` returns a Dict with selected information including the bounding box and items clicked on
-  `folium_static()`: takes a `folium.Map`, `folium.Figure`, or `branca.element.Figure` object and displays it in a Streamlit app.

    Note: `folium_static()` is based on the `_repr_html()` representation created in Folium. This function should be a strict subset the of functionality of the newer `st_folium()` function. It is recommended that users switch to `st_folium()` as soon as possible, as `folium_static()` will likely be deprecated.

    If there is a reason why `folium_static()` needs to remain, please leave a GitHub issue describing your use case.

## Example

![streamlit_folium example](https://raw.githubusercontent.com/randyzwitch/streamlit-folium/master/tests/visual_baseline/test_basic/first_test/baseline.png)


