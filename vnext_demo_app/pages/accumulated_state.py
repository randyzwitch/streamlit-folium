from __future__ import annotations

import folium
import streamlit as st
from folium.plugins import Draw

from streamlit_folium_vnext import st_folium_vnext

st.title("Accumulated State")
st.caption(
    "Clicks and drawn features are automatically accumulated across interactions. "
    "Click on markers to see object info, or click the map for bare coordinates."
)

col_left, col_right = st.columns([2, 1])

with col_left:
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)

    folium.Marker(
        [40.7128, -74.0060],
        popup="<b>NYC City Hall</b>",
        tooltip="City Hall",
    ).add_to(m)

    folium.Marker(
        [40.7484, -73.9856],
        popup="<b>Empire State Building</b>",
        tooltip="Empire State",
    ).add_to(m)

    folium.CircleMarker(
        [40.6892, -74.0445],
        radius=10,
        color="green",
        fill=True,
        fill_color="green",
        fill_opacity=0.6,
        popup="Statue of Liberty",
        tooltip="Liberty",
    ).add_to(m)

    Draw(export=False).add_to(m)

    result = st_folium_vnext(
        m,
        key="acc-map",
        height=500,
        subscribe=["click", "draw.created", "draw.edited", "draw.deleted"],
        state={"clicks": [], "drawn_features": []},
    )

with col_right:
    st.subheader("Accumulated Clicks")
    clicks = result.state.get("clicks", []) if result else []
    if clicks:
        for i, c in enumerate(clicks):
            obj = c.get("object")
            label = (
                f"{obj['kind']} ({obj.get('tooltip') or obj.get('id', '?')})"
                if obj
                else "map"
            )
            st.text(f"{i + 1}. [{label}] ({c['lat']:.5f}, {c['lng']:.5f})")
    else:
        st.info("Click on the map or markers to accumulate points.")

    st.subheader("Drawn Features")
    features = result.state.get("drawn_features", []) if result else []
    if features:
        st.metric("Feature count", len(features))
        st.json(features)
    else:
        st.info("Draw shapes to see them here.")

    if st.button("Clear accumulated state"):
        sk = "_stf_vnext_state_acc-map"
        if sk in st.session_state:
            del st.session_state[sk]
        st.rerun()

st.divider()
st.subheader("Latest Event (transient)")
if result and result.event:
    st.json(result.event)
else:
    st.caption("No event this rerun.")

st.subheader("View State")
if result:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Center Lat", f"{result.center[0]:.4f}" if result.center else "—")
    with c2:
        st.metric("Center Lng", f"{result.center[1]:.4f}" if result.center else "—")
    with c3:
        st.metric("Zoom", result.zoom if result.zoom else "—")

with st.expander("Show code"):
    st.code(
        """\
import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium_vnext import st_folium_vnext

m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)
folium.Marker([40.7128, -74.0060], tooltip="City Hall").add_to(m)
folium.CircleMarker([40.6892, -74.0445], radius=10, color="green",
                    fill=True, tooltip="Liberty").add_to(m)
Draw(export=False).add_to(m)

result = st_folium_vnext(
    m, key="acc-map", height=500,
    subscribe=["click", "draw.created", "draw.edited", "draw.deleted"],
    state={"clicks": [], "drawn_features": []},
)

# result.state persists across reruns via st.session_state
clicks = result.state["clicks"]            # list of click payloads
features = result.state["drawn_features"]  # list of drawn GeoJSON features
""",
        language="python",
    )
