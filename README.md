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


[<img src="https://py.cafe/logos/pycafe_logo.png" alt="PyCafe logo" width="24" height="24"> Run and edit this example in Py.Cafe](https://py.cafe/maartenbreddels/streamlit-folium-geospatial-visualizations)

![streamlit_folium example](https://raw.githubusercontent.com/randyzwitch/streamlit-folium/master/tests/visual_baseline/test_basic/first_test/baseline.png)


## Contributing

All of the necessary commands to get the project running are in the [Taskfile](https://taskfile.dev/).

### Linting and formatting

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

To run ruff, you can use the following command:

```bash
task lint
```

### Running tests

To run the tests, you can use the following command:

```bash
task test
```

### Adding tests

If you add a new feature, or fix a bug, please add a test to ensure that the feature works as expected.

The pattern for creating tests is to use the example streamlit app, and use
[playwright](https://playwright.dev/python/docs/intro) to create and
run tests on the app.

These tests are primarily located in the `tests/frontend.py` file.

If you are making a change that only affects the python code, you can
run the playwright [codegen](https://playwright.dev/python/docs/codegen) tool to
help generate the tests by running `task generate-tests`.

If you are making a change that affects the javascript code, you need to set up
folium to use your local frontend code. This can be done by:

1. Edit `streamlit_folium/__init__.py` to set `_RELEASE = False`
2. Run `task generate-tests-frontend`
3. Add tests as appropriate in `tests/frontend.py`
4. Run `task test-frontend` to run the tests
5. Set `_RELEASE = True` in `streamlit_folium/__init__.py` before opening a PR
