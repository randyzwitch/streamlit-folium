import { Streamlit, RenderData } from "streamlit-component-lib"
import { debounce } from "underscore"
import { circleToPolygon } from "./circle-to-polygon"

type GlobalData = {
  lat_lng_clicked: any
  last_object_clicked: any
  last_active_drawing: any
  all_drawings: any
  zoom: any
  drawn_items: any
  last_circle_radius: number | null
  last_circle_polygon: any
}

declare global {
  interface Window {
    __GLOBAL_DATA__: GlobalData
    initComponent: any
    map: any
    drawnItems: any
  }
}

function onMapClick(e: any) {
  const global_data = window.__GLOBAL_DATA__
  global_data.lat_lng_clicked = e.latlng
  debouncedUpdateComponentValue(window.map)
}

let debouncedUpdateComponentValue = debounce(updateComponentValue, 250)

function updateComponentValue(map: any) {
  const global_data = window.__GLOBAL_DATA__
  let bounds = map.getBounds()
  let zoom = map.getZoom()
  Streamlit.setComponentValue({
    last_clicked: global_data.lat_lng_clicked,
    last_object_clicked: global_data.last_object_clicked,
    all_drawings: global_data.all_drawings,
    last_active_drawing: global_data.last_active_drawing,
    bounds: bounds,
    zoom: zoom,
    last_circle_radius: global_data.last_circle_radius,
    last_circle_polygon: global_data.last_circle_polygon,
    center: map.getCenter(),
  })
}

function onMapMove(e: any) {
  debouncedUpdateComponentValue(window.map)
}

function onDraw(e: any) {
  const global_data = window.__GLOBAL_DATA__

  var type = e.layerType,
    layer = e.layer

  if (type === "circle") {
    var center: [number, number] = [layer._latlng.lng, layer._latlng.lat]
    var radius = layer.options.radius // In km
    var polygon = circleToPolygon(center, radius)
    global_data.last_circle_radius = radius / 1000 // Convert to km to match what UI shows
    global_data.last_circle_polygon = polygon
  }
  return onLayerClick(e)
}

function onLayerClick(e: any) {
  const global_data = window.__GLOBAL_DATA__
  global_data.last_object_clicked = e.latlng
  let details: Array<any> = []
  if (e.layer && e.layer.toGeoJSON) {
    global_data.last_active_drawing = e.layer.toGeoJSON()
  }
  if (window.drawnItems.toGeoJSON) {
    details = window.drawnItems.toGeoJSON().features
  }
  debugger
  global_data.all_drawings = details
  debouncedUpdateComponentValue(window.map)
}

window.initComponent = (map: any) => {
  map.on("click", onMapClick)
  map.on("moveend", onMapMove)
  for (let key in map._layers) {
    let layer = map._layers[key]
    layer.on("click", onLayerClick)
  }
  map.on("draw:created", onDraw)
  map.on("draw:edited", onDraw)
  map.on("draw:deleted", onDraw)

  Streamlit.setFrameHeight()
  updateComponentValue(map)
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event: Event): void {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail

  const fig: string = data.args["fig"]
  const height: number = data.args["height"]
  const width: number = data.args["width"]

  if (!window.map) {
    // Only run this if the map hasn't already been created (and thus the global
    //data hasn't been initialized)
    const div1 = document.getElementById("map_div")
    const div2 = document.getElementById("map_div2")
    if (div2) {
      div2.style.height = `${height}px`
      div2.style.width = `${width}px`
    }
    if (div1) {
      div1.style.height = `${height}px`
      div1.style.width = `${width}px`

      if (fig.indexOf("document.getElementById('export')") !== -1) {
        let a = document.createElement("a")
        a.href = "#"
        a.id = "export"
        a.innerHTML = "Export"
        document.body.appendChild(a)
      }

      const render_script = document.createElement("script")
      // HACK -- update the folium-generated JS to add, most importantly,
      // the map to this global variable so that it can be used elsewhere
      // in the script.

      window.__GLOBAL_DATA__ = {
        lat_lng_clicked: null,
        last_object_clicked: null,
        all_drawings: null,
        last_active_drawing: null,
        zoom: null,
        drawn_items: [],
        last_circle_radius: null,
        last_circle_polygon: null,
      }
      // The folium-generated script creates a variable called "map_div", which
      // is the actual Leaflet map.
      render_script.innerHTML =
        fig + `window.map = map_div; window.initComponent(map_div);`
      document.body.appendChild(render_script)
    }
  }
}

// Attach our `onRender` handler to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
