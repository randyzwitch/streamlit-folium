from __future__ import annotations

import folium
import streamlit as st

from streamlit_folium_vnext import st_folium_vnext

st.set_page_config(page_title="Click Events", layout="wide")
st.title("Click Events")
st.caption("Click anywhere on the map to see the coordinates.")

m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)

folium.Marker(
    [40.7128, -74.0060],
    popup="NYC City Hall",
    tooltip="Click me!",
).add_to(m)

result = st_folium_vnext(
    m,
    key="click-map",
    height=500,
    subscribe=["click"],
)

if result and result.event and result.event.get("type") == "click":
    st.session_state["last_click"] = result.event

last_click = st.session_state.get("last_click")
if last_click:
    payload = last_click["payload"]
    obj = payload.get("object")
    if obj:
        st.success(
            f"Clicked **{obj['kind']}** ({obj.get('tooltip') or obj.get('id', '')}) at: **{payload['lat']:.6f}, {payload['lng']:.6f}**"
        )
    else:
        st.success(f"Clicked map at: **{payload['lat']:.6f}, {payload['lng']:.6f}**")
else:
    st.info("Click on the map to see coordinates here.")

st.subheader("Raw Event")
st.json(last_click if last_click else {})

with st.expander("Show code"):
    st.code(
        """\
import folium
import streamlit as st
from streamlit_folium_vnext import st_folium_vnext

m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)
folium.Marker([40.7128, -74.0060], tooltip="Click me!").add_to(m)

result = st_folium_vnext(m, key="click-map", height=500, subscribe=["click"])

# result.event is transient — only set on the rerun triggered by the click
if result and result.event and result.event.get("type") == "click":
    payload = result.event["payload"]
    obj = payload.get("object")
    if obj:
        print(f"Clicked {obj['kind']} at {payload['lat']:.6f}, {payload['lng']:.6f}")
    else:
        print(f"Clicked map at {payload['lat']:.6f}, {payload['lng']:.6f}")
""",
        language="python",
    )
