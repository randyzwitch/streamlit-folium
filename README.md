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
-  `folium_static()`: takes a `folium.Map`, `folium.Figure`, or `branca.element.Figure` object and displays it in a Streamlit app using the `_repr_html()` representation created in Folium. This function should be a strict subset the of functionality of the newer `st_folium()` function, but is great for testing to ensure you have the correct Folium syntax.

## Example


[<img src="https://py.cafe/logos/pycafe_logo.png" alt="PyCafe logo" width="24" height="24"> Run and edit this example in Py.Cafe](https://py.cafe/maartenbreddels/streamlit-folium-geospatial-visualizations)

![streamlit_folium example](https://raw.githubusercontent.com/randyzwitch/streamlit-folium/master/tests/visual_baseline/test_basic/first_test/baseline.png)


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.
