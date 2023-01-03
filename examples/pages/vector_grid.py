import folium
from folium.plugins import VectorGridProtobuf

from streamlit_folium import st_folium

m = folium.Map(location=(30, 20), zoom_start=4)
url = "https://area.uqcom.jp/api2/rakuten/{z}/{x}/{y}.mvt"
vc = VectorGridProtobuf(url, "test").add_to(m)

st_folium(m, width=2000, height=500, returned_objects=[])
