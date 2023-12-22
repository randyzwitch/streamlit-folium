import { RenderData, Streamlit } from "streamlit-component-lib"
import { debounce } from "underscore"
import { circleToPolygon } from "./circle-to-polygon"
import { Layer } from "leaflet"

type GlobalData = {
  lat_lng_clicked: any
  last_object_clicked: any
  last_object_clicked_tooltip: string | null
  last_object_clicked_popup: string | null
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
  last_layer_control: any
}

declare global {
  interface Window {
    __GLOBAL_DATA__: GlobalData
    initComponent: any
    map: any
    drawnItems: any
    feature_group: any
    layer_control: any
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
    last_object_clicked_popup: global_data.last_object_clicked_popup,
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
  var span = document.createElement("span")
  span.innerHTML = s
  return (span.textContent || span.innerText).trim()
}

function onDraw(e: any) {
  const global_data = window.__GLOBAL_DATA__

  var type = e.layerType,
    layer = e.layer

  if (type === "circle") {
    var center: [number, number] = [layer._latlng.lng, layer._latlng.lat]
    var radius = layer.options.radius // In meters
    var polygon = circleToPolygon(center, radius)

    // Ensure that radius gets added to circle properties when converted to GeoJSON
    var feature = (e.layer.feature = e.layer.feature || {})
    feature.type = "Feature"
    feature.properties = feature.properties || {}
    feature.properties["radius"] = radius

    global_data.last_circle_radius = radius / 1000 // Convert to km to match what UI shows
    global_data.last_circle_polygon = polygon
  }
  return onLayerClick(e)
}

function onLayerClick(e: any) {
  const global_data = window.__GLOBAL_DATA__
  global_data.last_object_clicked = e.latlng

  if (e.sourceTarget._tooltip && e.sourceTarget._tooltip._content) {
    let tooltip_text = extractContent(e.sourceTarget.getTooltip().getContent())
    global_data.last_object_clicked_tooltip = tooltip_text
  } else if (e.target._tooltip && e.target._tooltip._content) {
    let tooltip_text = e.target.getTooltip().getContent()(
      e.sourceTarget
    ).innerText
    global_data.last_object_clicked_tooltip = tooltip_text
  }

  if (e.sourceTarget._popup && e.sourceTarget._popup._content) {
    let popup_text = e.sourceTarget.getPopup().getContent().innerText
    global_data.last_object_clicked_popup = popup_text
  } else if (e.target._popup && e.target._popup._content) {
    let popup_text = e.target.getPopup().getContent()(e.sourceTarget).innerText
    global_data.last_object_clicked_popup = popup_text
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

window.initComponent = (map: any, return_on_hover: boolean) => {
  map.on("click", onMapClick)
  map.on("moveend", onMapMove)
  for (let key in map._layers) {
    let layer = map._layers[key]
    layer.on("click", onLayerClick)
    if (return_on_hover) {
      layer.on("mouseover", onLayerClick)
    }
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
  const return_on_hover: boolean = data.args["return_on_hover"]
  const layer_control: string = data.args["layer_control"]

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
        last_object_clicked_popup: null,
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
        last_layer_control: null,
      }
      if (script.indexOf("map_div2") !== -1) {
        parent_div?.classList.remove("single")
        parent_div?.classList.add("double")
      }

      // The folium-generated script creates a variable called "map_div", which
      // is the actual Leaflet map.
      render_script.innerHTML =
        script +
        `window.map = map_div; window.initComponent(map_div, ${return_on_hover});`
      document.body.appendChild(render_script)
      const html_div = document.createElement("div")
      html_div.innerHTML = html
      document.body.appendChild(html_div)
    }
  }

  if (
    feature_group !== window.__GLOBAL_DATA__.last_feature_group ||
    layer_control !== window.__GLOBAL_DATA__.last_layer_control
  ) {
    if (window.feature_group && window.feature_group.length > 0) {
      window.feature_group.forEach((layer: Layer) => {
        window.map.removeLayer(layer);
      });
    }

    if (window.layer_control) {
      window.map.removeControl(window.layer_control)
    }

    window.__GLOBAL_DATA__.last_feature_group = feature_group
    window.__GLOBAL_DATA__.last_layer_control = layer_control

    if (feature_group){
      // Though using `eval` is generally a bad idea, we're using it here
      // because we're evaluating code that we've generated ourselves on the
      // Python side. This is safe because we're not evaluating user input, so this
      // couldn't be used to execute arbitrary code.

      // eslint-disable-next-line
      eval(feature_group + layer_control)
      for (let key in window.map._layers) {
        let layer = window.map._layers[key]
        layer.off("click", onLayerClick)
        layer.on("click", onLayerClick)
        if (return_on_hover) {
          layer.off("mouseover", onLayerClick)
          layer.on("mouseover", onLayerClick)
        }
      }
    } else {
      // eslint-disable-next-line
      eval(layer_control)
    }
  }

  var view_changed = false
  var new_zoom = window.map.getZoom()
  if (zoom && zoom !== window.__GLOBAL_DATA__.last_zoom) {
    new_zoom = zoom
    window.__GLOBAL_DATA__.last_zoom = zoom
    view_changed = true
  }

  var new_center = window.map.getCenter()
  if (
    center &&
    JSON.stringify(center) !==
      JSON.stringify(window.__GLOBAL_DATA__.last_center)
  ) {
    new_center = center
    window.__GLOBAL_DATA__.last_center = center
    view_changed = true
  }

  if (view_changed) {
    window.map.setView(new_center, new_zoom)
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
