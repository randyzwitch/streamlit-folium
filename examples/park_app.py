from dataclasses import dataclass
from typing import Dict, List, Optional

import folium
import requests
import streamlit as st

from streamlit_folium import st_folium

st.set_page_config(layout="wide")


@st.cache_resource
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


#############################
# Streamlit app
#############################

"## National Parks in the United States"

"""
The National Parks Service provides an
[API](https://www.nps.gov/subjects/digital/nps-data-api.htm) to programmatically explore
NPS data.

We can take data about each park and display it on the map _conditionally_ based on
whether it is in the viewport.

---
"""

# define layout
c1, c2 = st.columns(2)

# get and cache data from API
parks = get_data()

# layout map
with c1:
    """(_Click on a pin to bring up more information_)"""
    m = folium.Map(location=[39.949610, -75.150282], zoom_start=4)

    for park in parks:
        popup = folium.Popup(
            f"""
                  <a href="{park["url"]}" target="_blank">{park["fullName"]}</a><br>
                  <br>
                  {park["operatingHours"][0]["description"]}<br>
                  <br>
                  Phone: {park["contacts"]["phoneNumbers"][0]["phoneNumber"]}<br>
                  """,
            max_width=250,
        )
        folium.Marker([park["latitude"], park["longitude"]], popup=popup).add_to(m)

    map_data = st_folium(m, key="fig1", width=700, height=700)

# get data from map for further processing
map_bounds = Bounds.from_dict(map_data["bounds"])

# when a point is clicked, display additional information about the park
try:
    point_clicked: Optional[Point] = Point.from_dict(map_data["last_object_clicked"])

    if point_clicked is not None:
        with st.spinner(text="loading image..."):
            for park in parks:
                if park["_point"].is_close_to(point_clicked):
                    with c2:
                        f"""### _{park["fullName"]}_"""
                        park["description"]
                        st.image(
                            park["images"][0]["url"],
                            caption=park["images"][0]["caption"],
                        )
                        st.expander("Show park full details").write(park)
except TypeError:
    point_clicked = None

# even though there is a c1 reference above, we can do it again
# output will get appended after original content
with c1:
    parks_in_view: List[Dict] = []
    for park in parks:
        if map_bounds.contains_point(park["_point"]):
            parks_in_view.append(park)

    "Parks visible:", len(parks_in_view)
    "Bounding box:", map_bounds
