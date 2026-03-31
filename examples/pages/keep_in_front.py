import folium
import vega_datasets
from altair import Chart

from streamlit_folium import st_folium

# load built-in dataset as a pandas DataFrame
cars = vega_datasets.data.cars()

scatter = (
    Chart(cars)
    .mark_circle()
    .encode(
        x="Horsepower",
        y="Miles_per_Gallon",
        color="Origin",
    )
)

vega_lite = folium.VegaLite(
    scatter,
    width="100%",
    height="100%",
)

m = folium.Map(location=[-27.5717, -48.6256])

marker = folium.Marker([-27.57, -48.62])

popup = folium.Popup()

vega_lite.add_to(popup)
popup.add_to(marker)

marker.add_to(m)

st_folium(m, debug=True)
