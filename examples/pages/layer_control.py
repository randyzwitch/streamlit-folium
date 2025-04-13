import folium
import streamlit as st
from folium import WmsTileLayer
from folium.plugins import Draw

from streamlit_folium import st_folium

# Set page configurations
st.set_page_config(
    page_title="streamlit-folium documentation: LayerControl",
)

# WMTS layers dictionary
LAYER_WMTS: dict[str, dict] = {
    "KATASTER-Farbig": {
        "wmts_url": "https://geodienste.ch/db/avc_0/deu",
        "layer_name": "daten",
        "legend_url": None,
    },
    "SWISS-IMAGE": {
        "wmts_url": "https://wms.geo.admin.ch/",
        "layer_name": "ch.swisstopo.swissimage",
        "legend_url": None,
    },
    "Solarenergie: Eignung Dächer": {
        "wmts_url": "https://wms.geo.admin.ch/",
        "layer_name": "ch.bfe.solarenergie-eignung-daecher",
        "legend_url": "https://api3.geo.admin.ch/static/images/legends/ch.bfe.solarenergie-eignung-daecher_de.png",
    },
    "Solarenergie: Eignung Fassaden": {
        "wmts_url": "https://wms.geo.admin.ch/g",
        "layer_name": "ch.bfe.solarenergie-eignung-fassaden",
        "legend_url": "https://api3.geo.admin.ch/static/images/legends/ch.bfe.solarenergie-eignung-fassaden_de.png",
    },
    "Solare Einstrahlung horizontal": {
        "wmts_url": "https://wms.geo.admin.ch/",
        "layer_name": "ch.bfe.solarenergie-einstrahlung_0_grad",
        "legend_url": "https://api3.geo.admin.ch/static/images/legends/ch.bfe.solarenergie-einstrahlung_0_grad_de.png",
    },
    "Solare Einstrahlung 30° Neigung Süd": {
        "wmts_url": "https://wms.geo.admin.ch/",
        "layer_name": "ch.bfe.solarenergie-einstrahlung_30_grad",
        "legend_url": "https://api3.geo.admin.ch/static/images/legends/ch.bfe.solarenergie-einstrahlung_30_grad_de.png",
    },
    "Solare Einstrahlung 75° Neigung Süd": {
        "wmts_url": "https://wms.geo.admin.ch/",
        "layer_name": "ch.bfe.solarenergie-einstrahlung_75_grad",
        "legend_url": "https://api3.geo.admin.ch/static/images/legends/ch.bfe.solarenergie-einstrahlung_75_grad_de.png",
    },
    "Solare Einstrahlung 90° Neigung Süd": {
        "wmts_url": "https://wms.geo.admin.ch/",
        "layer_name": "ch.bfe.solarenergie-einstrahlung_90_grad",
        "legend_url": "https://api3.geo.admin.ch/static/images/legends/ch.bfe.solarenergie-einstrahlung_90_grad_de.png",
    },
}

m = folium.Map(location=[47.377512, 8.540670], zoom_start=15, max_zoom=20)

selected_layers = LAYER_WMTS

for i, layer in enumerate(selected_layers):
    layer_info = LAYER_WMTS[layer]

    st.write("Layer Info:", layer_info)

    if layer_info.get("wmts_url") and layer_info.get("layer_name"):
        try:
            WmsTileLayer(
                url=layer_info["wmts_url"],
                layers=layer_info["layer_name"],
                name=layer,
                fmt="image/png",
                transparent=True,
                overlay=True,
                control=True,
                version="1.3.0",
                show=i == 0,
                max_zoom=20,
            ).add_to(m)
        except Exception as e:
            st.error(f"Error adding layer {layer}: {e}")
    else:
        st.warning(f"Missing URL or layer for {layer}")

Draw(export=True).add_to(m)

folium.LayerControl(position="topright").add_to(m)

data = st_folium(m)
st.write(data)
