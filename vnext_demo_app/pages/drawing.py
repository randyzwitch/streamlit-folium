from __future__ import annotations

import folium
import streamlit as st
from folium.plugins import Draw

from streamlit_folium_vnext import st_folium_vnext

st.title("Drawing Tools")
st.caption("Use the draw toolbar to create shapes, then edit or delete them.")

m = folium.Map(location=[51.505, -0.09], zoom_start=13)
Draw(export=False).add_to(m)

result = st_folium_vnext(
    m,
    key="draw-map",
    height=500,
    subscribe=["draw.created", "draw.edited", "draw.deleted"],
)

if result and result.event:
    event_type = result.event.get("type", "")
    if event_type == "draw.created":
        st.success(
            f"Shape created: **{result.event['payload'].get('layerType', '?')}**"
        )
    elif event_type == "draw.edited":
        count = len(result.event["payload"].get("features", []))
        st.info(f"Edited **{count}** feature(s)")
    elif event_type == "draw.deleted":
        count = len(result.event["payload"].get("features", []))
        st.warning(f"Deleted **{count}** feature(s)")
    elif event_type == "click":
        obj = result.event["payload"].get("object")
        if obj and obj.get("kind") == "drawn":
            geom_type = (
                obj["geojson"]["geometry"]["type"] if obj.get("geojson") else "?"
            )
            st.info(f"Clicked drawn shape — geometry type: **{geom_type}**")
else:
    st.info("Draw a shape on the map to see events here.")

st.subheader("Raw Event")
st.json(result.event if result and result.event else {})

with st.expander("Show code"):
    st.code(
        """\
import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium_vnext import st_folium_vnext

m = folium.Map(location=[51.505, -0.09], zoom_start=13)
Draw(export=False).add_to(m)

result = st_folium_vnext(
    m, key="draw-map", height=500,
    subscribe=["draw.created", "draw.edited", "draw.deleted"],
)

# result.event is transient — only set on the rerun triggered by the draw action
if result and result.event:
    event_type = result.event.get("type", "")
    if event_type == "draw.created":
        geojson = result.event["payload"]["geojson"]
    elif event_type == "draw.edited":
        features = result.event["payload"]["features"]
    elif event_type == "draw.deleted":
        features = result.event["payload"]["features"]
    elif event_type == "click":
        obj = result.event["payload"]["object"]
        # obj = {"kind": "drawn", "geojson": {...}}
""",
        language="python",
    )
