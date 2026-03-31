# streamlit-folium Examples

This directory contains example applications demonstrating streamlit-folium functionality.

## Installation

Install the required dependencies:

```bash
# Using pip
pip install "streamlit-folium[examples]"

# Using uv
uv pip install "streamlit-folium[examples]"
```

## Running Examples

```bash
# Main example app with all examples
streamlit run streamlit_app.py

# Standalone park demo
streamlit run park_app.py
```

## Navigation System

The example app uses Streamlit's new `st.navigation` and `st.Page` APIs to create a structured, navigable multi-page experience:

```python
# Define pages with icons
basic_examples = [
    st.Page(home_example, title="Home Example", icon="home"),
    st.Page("pages/static_map.py", title="Static Map", icon=":material/public:"),
]

# Group pages into sections
pages = {
    "Basic Examples": basic_examples,
    "Interactive Features": interactive_features,
    # ... other sections
}

# Configure the navigation and get current page
current_page = st.navigation(pages)

# Run the selected page
current_page.run()
```

### Example Organization

Examples are organized into logical groups:

- **Basic Examples**: Simple maps, popups, and responsive layouts
- **Interactive Features**: Draw support, callbacks, and user interactions
- **Dynamic Maps**: Real-time updates and movement capabilities
- **Layers & Styling**: Layer controls and visualization customization
- **GeoJSON & Overlays**: Geographic data display and image overlays
- **Miscellaneous**: Other specialized examples

Each example demonstrates specific features of the streamlit-folium package.

## Creating Your Own Examples

To add a new example, either:

1. Create a new Python file in the `pages/` directory
2. Add it to the appropriate section in `streamlit_app.py`

See the existing examples for guidance on structure and implementation.