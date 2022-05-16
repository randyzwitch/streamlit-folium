import folium

from streamlit_folium import st_folium

m = folium.Map([45, 0], zoom_start=4)

folium.Marker([45, -30], popup="inline implicit popup").add_to(m)

folium.CircleMarker(
    location=[45, -10],
    radius=25,
    fill=True,
    popup=folium.Popup("inline explicit Popup"),
).add_to(m)

ls = folium.PolyLine(
    locations=[[43, 7], [43, 13], [47, 13], [47, 7], [43, 7]], color="red"
)

ls.add_child(folium.Popup("outline Popup on Polyline"))
ls.add_to(m)

gj = folium.GeoJson(
    data={"type": "Polygon", "coordinates": [[[27, 43], [33, 43], [33, 47], [27, 47]]]}
)

gj.add_child(folium.Popup("outline Popup on GeoJSON"))
gj.add_to(m)

st_folium(m)
