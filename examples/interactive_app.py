from dataclasses import dataclass
from typing import Dict, List, Optional

import folium
import requests
import streamlit as st
from streamlit_folium import st_folium


@st.experimental_singleton
def get_data() -> List[Dict]:
    api_key = st.secrets["api_key"]
    url = f"https://developer.nps.gov/api/v1/parks?api_key={api_key}&limit=500"
    resp = requests.get(url)
    data = resp.json()["data"]
    parks = [park for park in data if park["designation"] == "National Park"]

    for park in parks:
        park["_point"] = Point.from_dict(park)

    return parks


@dataclass
class Point:
    lat: float
    lon: float

    @classmethod
    def from_dict(cls, data: Dict) -> "Point":
        if "lat" in data:
            return cls(float(data["lat"]), float(data["lng"]))
        elif "latitude" in data:
            return cls(float(data["latitude"]), float(data["longitude"]))
        else:
            raise NotImplementedError(data.keys())

    def is_close_to(self, other: "Point") -> bool:
        close_lat = self.lat - 0.0001 <= other.lat <= self.lat + 0.0001
        close_lon = self.lon - 0.0001 <= other.lon <= self.lon + 0.0001
        return close_lat and close_lon


@dataclass
class Bounds:
    south_west: Point
    north_east: Point

    def contains_point(self, point: Point) -> bool:
        in_lon = self.south_west.lon <= point.lon <= self.north_east.lon
        in_lat = self.south_west.lat <= point.lat <= self.north_east.lat

        return in_lon and in_lat

    @classmethod
    def from_dict(cls, data: Dict) -> "Bounds":
        return cls(
            Point.from_dict(data["_southWest"]), Point.from_dict(data["_northEast"])
        )


parks = get_data()

"## Click on one of the markers"

m = folium.Map(location=[39.949610, -75.150282], zoom_start=5)

for park in parks:
    tooltip = park["name"]
    folium.Marker(
        [park["latitude"], park["longitude"]], popup=park["name"], tooltip=tooltip
    ).add_to(m)


map_data = st_folium(m, key="fig1", width=700, height=700)

map_bounds = Bounds.from_dict(map_data["bounds"])

try:
    point_clicked: Optional[Point] = Point.from_dict(map_data["last_object_clicked"])
except TypeError:
    point_clicked = None

if point_clicked is not None:
    with st.spinner(text="loading image..."):
        for park in parks:
            if park["_point"].is_close_to(point_clicked):
                st.image(park["images"][0]["url"])
                st.expander("Show park full details").write(park)

parks_in_view: List[Dict] = []
for park in parks:
    if map_bounds.contains_point(park["_point"]):
        parks_in_view.append(park)

st.sidebar.write("## Parks visible")
for park in parks_in_view:
    with st.sidebar.expander(park["name"]):
        st.write(park["description"])

st.sidebar.write("---")

st.sidebar.expander("Show map data").write(map_data)
