import { Streamlit, RenderData } from "streamlit-component-lib"
import { debounce } from "underscore"
import { circleToPolygon } from "./circle-to-polygon"

type GlobalData = {
  lat_lng_clicked: any
  last_object_clicked: any
  last_object_clicked_tooltip: string | null
  last_active_drawing: any
  all_drawings: any
  zoom: any
  last_circle_radius: number | null
  last_circle_polygon: any
  returned_objects: Array<string>
  previous_data: any
  last_zoom: any
  last_center: any
  last_feature_group: any
}

declare global {
  interface Window {
    __GLOBAL_DATA__: GlobalData
    initComponent: any
    map: any
    drawnItems: any
    feature_group: any
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
  let previous_data = global_data.previous_data
  let bounds = map.getBounds()
  let zoom = map.getZoom()
  let _data = {
    last_clicked: global_data.lat_lng_clicked,
    last_object_clicked: global_data.last_object_clicked,
    last_object_clicked_tooltip: global_data.last_object_clicked_tooltip,
    all_drawings: global_data.all_drawings,
    last_active_drawing: global_data.last_active_drawing,
    bounds: bounds,
    zoom: zoom,
    last_circle_radius: global_data.last_circle_radius,
    last_circle_polygon: global_data.last_circle_polygon,
    center: map.getCenter(),
  }

  let to_return = global_data.returned_objects

  // Filter down the data to only that data passed in the returned_objects list
  let data: any = {}
  if (to_return) {
    data = Object.fromEntries(
      Object.entries(_data).filter(([key]) =>
        global_data.returned_objects.includes(key)
      )
    )
  } else {
    data = _data
  }
  if (JSON.stringify(previous_data) !== JSON.stringify(data)) {
    global_data.previous_data = data
    Streamlit.setComponentValue(data)
  }
}

function onMapMove(e: any) {
  debouncedUpdateComponentValue(window.map)
}

function extractContent(s: string) {
  var span = document.createElement('span');
  span.innerHTML = s;
  return (span.textContent || span.innerText).trim();
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

  if (e.sourceTarget._tooltip && e.sourceTarget._tooltip._content) {
    let tooltip_text = extractContent(e.sourceTarget._tooltip._content);
    global_data.last_object_clicked_tooltip = tooltip_text;
  }

  let details: Array<any> = []
  if (e.layer && e.layer.toGeoJSON) {
    global_data.last_active_drawing = e.layer.toGeoJSON()
  }
  if (window.drawnItems.toGeoJSON) {
    details = window.drawnItems.toGeoJSON().features
  }
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

  const script: string = data.args["script"]
  const height: number = data.args["height"]
  const width: number = data.args["width"]
  const html: string = data.args["html"]
  const returned_objects: Array<string> = data.args["returned_objects"]
  const _default: any = data.args["default"]
  const zoom: any = data.args["zoom"]
  const center: any = data.args["center"]
  const feature_group: string = data.args["feature_group"]

  if (!window.map) {
    // Only run this if the map hasn't already been created (and thus the global
    //data hasn't been initialized)
    const parent_div = document.getElementById("parent")
    const div1 = document.getElementById("map_div")
    const div2 = document.getElementById("map_div2")
    if (div2) {
      div2.style.height = `${height}px`
      div2.style.width = `${width}px`
    }
    if (div1) {
      div1.style.height = `${height}px`
      div1.style.width = `${width}px`

      if (script.indexOf("document.getElementById('export')") !== -1) {
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
        last_object_clicked_tooltip: null,
        all_drawings: null,
        last_active_drawing: null,
        zoom: null,
        last_circle_radius: null,
        last_circle_polygon: null,
        returned_objects: returned_objects,
        previous_data: _default,
        last_zoom: null,
        last_center: null,
        last_feature_group: null,
      }
      if (script.indexOf("map_div2") !== -1) {
        parent_div?.classList.remove("single")
        parent_div?.classList.add("double")
      }

      // The folium-generated script creates a variable called "map_div", which
      // is the actual Leaflet map.
      render_script.innerHTML =
        script + `window.map = map_div; window.initComponent(map_div);`
      document.body.appendChild(render_script)
      const html_div = document.createElement("div")
      html_div.innerHTML = html
      document.body.appendChild(html_div)
    }
  }

  if (
    feature_group &&
    feature_group !== window.__GLOBAL_DATA__.last_feature_group
  ) {
    if (window.feature_group) {
      window.map.removeLayer(window.feature_group)
    }
    // Though using `eval` is generally a bad idea, we're using it here
    // because we're evaluating code that we've generated ourselves on the
    // Python side. This is safe because we're not evaluating user input, so this
    // couldn't be used to execute arbitrary code.

    // eslint-disable-next-line
    eval(feature_group)
    window.__GLOBAL_DATA__.last_feature_group = feature_group
    for (let key in window.map._layers) {
      let layer = window.map._layers[key]
      layer.off("click", onLayerClick)
      layer.on("click", onLayerClick)
    }
  }

  if (zoom && zoom !== window.__GLOBAL_DATA__.last_zoom) {
    window.map.setZoom(zoom)
    window.__GLOBAL_DATA__.last_zoom = zoom
  }
  if (
    center &&
    JSON.stringify(center) !==
      JSON.stringify(window.__GLOBAL_DATA__.last_center)
  ) {
    window.map.panTo(center)
    window.__GLOBAL_DATA__.last_center = center
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
