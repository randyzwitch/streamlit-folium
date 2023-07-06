from __future__ import annotations

from pathlib import Path

import folium
import folium.features
import pandas as pd
import requests
import streamlit as st

from streamlit_folium import st_folium

p = Path(__file__).parent / "states.csv"
STATE_DATA = pd.read_csv(p)


st.set_page_config(layout="wide")

"# Dynamic Updates -- Click on a marker"

st.subheader(
    """Use new arguments `center`, `zoom`, and `feature_group_to_add` to update the map
    without re-rendering it."""
)


@st.cache_data
def _get_all_state_bounds() -> dict:
    url = "https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json"
    data = requests.get(url).json()
    return data


@st.cache_data
def get_state_bounds(state: str) -> dict:
    data = _get_all_state_bounds()
    state_entry = [f for f in data["features"] if f["properties"]["name"] == state][0]
    return {"type": "FeatureCollection", "features": [state_entry]}


def get_state_from_lat_lon(lat: float, lon: float) -> str:
    state_row = STATE_DATA[
        STATE_DATA.latitude.between(lat - 0.0001, lat + 0.0001)
        & STATE_DATA.longitude.between(lon - 0.0001, lon + 0.0001)
    ].iloc[0]
    return state_row["state"]


def get_population(state: str) -> int:
    return STATE_DATA.set_index("state").loc[state]["population"]


def main():
    if "last_object_clicked" not in st.session_state:
        st.session_state["last_object_clicked"] = None
    if "selected_state" not in st.session_state:
        st.session_state["selected_state"] = "Indiana"

    bounds = get_state_bounds(st.session_state["selected_state"])

    st.write(f"## {st.session_state['selected_state']}")
    population = get_population(st.session_state["selected_state"])
    st.write(f"### Population: {population:,}")

    center = None
    if st.session_state["last_object_clicked"]:
        center = st.session_state["last_object_clicked"]

    with st.echo(code_location="below"):
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

        # If you want to dynamically add or remove items from the map,
        # add them to a FeatureGroup and pass it to st_folium
        fg = folium.FeatureGroup(name="State bounds")
        fg.add_child(folium.features.GeoJson(bounds))

        capitals = STATE_DATA

        for capital in capitals.itertuples():
            fg.add_child(
                folium.Marker(
                    location=[capital.latitude, capital.longitude],
                    popup=f"{capital.capital}, {capital.state}",
                    tooltip=f"{capital.capital}, {capital.state}",
                    icon=folium.Icon(color="green")
                    if capital.state == st.session_state["selected_state"]
                    else None,
                )
            )

        out = st_folium(
            m,
            feature_group_to_add=fg,
            center=center,
            width=1200,
            height=500,
        )

    if (
        out["last_object_clicked"]
        and out["last_object_clicked"] != st.session_state["last_object_clicked"]
    ):
        st.session_state["last_object_clicked"] = out["last_object_clicked"]
        state = get_state_from_lat_lon(*out["last_object_clicked"].values())
        st.session_state["selected_state"] = state
        st.experimental_rerun()


if __name__ == "__main__":
    main()
