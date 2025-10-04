# WIP
from folium import JsCode

click = JsCode("""
    function onMapClick(e) {
        const global_data = window.__GLOBAL_DATA__
        global_data.lat_lng_clicked = e.latlng
        debouncedUpdateComponentValue(window.map)
        }
""")

move = JsCode("""
    function onMapMove(e) {
        debouncedUpdateComponentValue(window.map)
    }
""")
