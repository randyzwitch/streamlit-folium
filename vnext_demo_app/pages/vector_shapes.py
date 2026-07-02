from __future__ import annotations

import folium
import streamlit as st

from streamlit_folium_vnext import st_folium_vnext

st.title("Vector Shapes")
st.caption(
    "Circle (fixed-radius), Polyline, and Polygon layers. "
    "Click any shape to see its event payload."
)

m = folium.Map(location=[48.85, 2.35], zoom_start=5)

folium.Circle(
    location=[51.509, -0.118],
    radius=15_000,
    color="#2563eb",
    fill=True,
    fill_opacity=0.25,
    tooltip="London — 15 km radius",
    popup="<b>London</b><br>15 km circle",
).add_to(m)

folium.Circle(
    location=[48.857, 2.347],
    radius=10_000,
    color="#dc2626",
    fill=True,
    fill_opacity=0.25,
    tooltip="Paris — 10 km radius",
    popup="<b>Paris</b><br>10 km circle",
).add_to(m)

folium.Circle(
    location=[52.52, 13.405],
    radius=12_000,
    color="#16a34a",
    fill=True,
    fill_opacity=0.25,
    tooltip="Berlin — 12 km radius",
    popup="<b>Berlin</b><br>12 km circle",
).add_to(m)

folium.PolyLine(
    locations=[
        [51.509, -0.118],
        [50.846, 4.352],
        [48.857, 2.347],
    ],
    color="#7c3aed",
    weight=3,
    opacity=0.8,
    tooltip="London → Brussels → Paris",
).add_to(m)

folium.PolyLine(
    locations=[
        [48.857, 2.347],
        [50.113, 8.682],
        [52.52, 13.405],
    ],
    color="#ea580c",
    weight=3,
    opacity=0.8,
    dash_array="8 4",
    tooltip="Paris → Frankfurt → Berlin",
).add_to(m)

folium.Polygon(
    locations=[
        [53.55, 10.0],
        [52.37, 4.9],
        [51.05, 3.72],
        [50.85, 4.35],
        [48.86, 2.35],
        [48.21, 16.37],
        [52.52, 13.41],
        [53.55, 10.0],
    ],
    color="#0891b2",
    fill=True,
    fill_color="#0891b2",
    fill_opacity=0.1,
    weight=2,
    tooltip="Rough Central Europe polygon",
    popup="<b>Central Europe</b>",
).add_to(m)

result = st_folium_vnext(m, key="vector-shapes", height=520, subscribe=["click"])

if result and result.event and result.event.get("type") == "click":
    st.session_state["last_shape_click"] = result.event

last = st.session_state.get("last_shape_click")
if last:
    payload = last["payload"]
    obj = payload.get("object")
    if obj:
        kind = obj["kind"]
        if kind == "circle":
            st.success(f"Clicked **circle** — radius {obj.get('radius', '?')} m")
        elif kind == "polyline":
            st.success("Clicked **polyline**")
        elif kind == "polygon":
            st.success("Clicked **polygon**")
    else:
        st.success(f"Clicked map at **{payload['lat']:.5f}, {payload['lng']:.5f}**")

    st.subheader("Raw Event")
    st.json(last)
else:
    st.info("Click a shape or the map to see its event here.")

with st.expander("Show code"):
    st.code(
        """\
import folium
import streamlit as st
from streamlit_folium_vnext import st_folium_vnext

m = folium.Map(location=[48.85, 2.35], zoom_start=5)

# Fixed-radius circle (meters, not pixels)
folium.Circle(
    location=[51.509, -0.118], radius=15_000,
    color="#2563eb", fill=True, tooltip="London — 15 km",
).add_to(m)

# Polyline connecting two cities
folium.PolyLine(
    locations=[[51.509, -0.118], [50.846, 4.352], [48.857, 2.347]],
    color="#7c3aed", weight=3, tooltip="London → Brussels → Paris",
).add_to(m)

# Filled polygon
folium.Polygon(
    locations=[[53.55,10.0],[52.37,4.9],[48.86,2.35],[52.52,13.41],[53.55,10.0]],
    color="#0891b2", fill=True, fill_opacity=0.1,
).add_to(m)

result = st_folium_vnext(m, key="vector-shapes", height=500, subscribe=["click"])
if result and result.event and result.event.get("type") == "click":
    obj = result.event["payload"].get("object")
    print(obj)  # {"kind": "circle"/"polyline"/"polygon", ...}
""",
        language="python",
    )
