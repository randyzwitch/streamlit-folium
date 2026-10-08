from __future__ import annotations

import folium
import folium.plugins
import streamlit as st

from streamlit_folium_vnext import st_folium_vnext

st.title("Marker Cluster")
st.caption("Zoom in/out to see markers cluster and uncluster automatically.")

CITIES = [
    (40.7128, -74.0060, "New York", "Largest city in the US"),
    (34.0522, -118.2437, "Los Angeles", "City of Angels"),
    (41.8781, -87.6298, "Chicago", "The Windy City"),
    (29.7604, -95.3698, "Houston", "Space City"),
    (33.4484, -112.0740, "Phoenix", "Valley of the Sun"),
    (39.9526, -75.1652, "Philadelphia", "City of Brotherly Love"),
    (29.4241, -98.4936, "San Antonio", "The Alamo City"),
    (32.7767, -96.7970, "Dallas", "Big D"),
    (30.2672, -97.7431, "Austin", "Live Music Capital"),
    (30.3322, -81.6557, "Jacksonville", "The River City"),
    (30.3960, -86.4958, "Fort Walton Beach", "Emerald Coast"),
    (36.1627, -86.7816, "Nashville", "Music City"),
    (35.1495, -90.0490, "Memphis", "Home of the Blues"),
    (38.2527, -85.7585, "Louisville", "Derby City"),
    (39.7684, -86.1581, "Indianapolis", "Racing Capital"),
    (39.9612, -82.9988, "Columbus", "Arch City"),
    (37.3382, -121.8863, "San Jose", "Capital of Silicon Valley"),
    (37.7749, -122.4194, "San Francisco", "The City by the Bay"),
    (47.6062, -122.3321, "Seattle", "The Emerald City"),
    (45.5051, -122.6750, "Portland", "City of Roses"),
    (44.9778, -93.2650, "Minneapolis", "City of Lakes"),
    (44.9537, -93.0900, "St. Paul", "The Capital City"),
    (43.0481, -76.1474, "Syracuse", "Salt City"),
    (42.3601, -71.0589, "Boston", "The Cradle of Liberty"),
    (42.8864, -78.8784, "Buffalo", "The Queen City"),
    (43.0962, -79.0377, "Niagara Falls", "Honeymoon Capital"),
    (38.9072, -77.0369, "Washington DC", "The Nation's Capital"),
    (39.2904, -76.6122, "Baltimore", "Charm City"),
    (35.2271, -80.8431, "Charlotte", "Queen City of the South"),
    (35.7796, -78.6382, "Raleigh", "City of Oaks"),
]

m = folium.Map(location=[39.5, -98.35], zoom_start=4)

mc = folium.plugins.MarkerCluster()
for lat, lng, name, desc in CITIES:
    folium.Marker(
        [lat, lng],
        tooltip=name,
        popup=folium.Popup(f"<b>{name}</b><br>{desc}", max_width=200),
    ).add_to(mc)
mc.add_to(m)

result = st_folium_vnext(m, key="cluster-map", height=550, subscribe=["click"])

if result and result.event:
    payload = result.event.get("payload", {})
    obj = payload.get("object", {})
    if obj.get("kind") == "marker_cluster_item":
        st.success(
            f"Clicked: **{obj.get('tooltip', '?')}** at {payload.get('lat'):.4f}, {payload.get('lng'):.4f}"
        )
else:
    st.info("Click a marker (zoom in first) to see its event here.")

st.subheader("Raw Event")
st.json(result.event if result and result.event else {})

with st.expander("Show code"):
    st.code(
        """\
import folium
import folium.plugins
import streamlit as st
from streamlit_folium_vnext import st_folium_vnext

m = folium.Map(location=[39.5, -98.35], zoom_start=4)
mc = folium.plugins.MarkerCluster()

for lat, lng, name in cities:
    folium.Marker([lat, lng], tooltip=name).add_to(mc)
mc.add_to(m)

result = st_folium_vnext(m, key="cluster-map", height=550, subscribe=["click"])
""",
        language="python",
    )
