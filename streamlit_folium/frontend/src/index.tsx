import { Streamlit, RenderData } from "streamlit-component-lib"
import { debounce } from "underscore";
//import "leaflet-draw";
import * as L from "leaflet";

let map: any = null;

type GlobalData = {
  map: any;
  lat_lng_clicked: any;
  last_object_clicked: any;
  last_active_drawing: any,
  all_drawings: any,
  bounds: any;
};

declare var __GLOBAL_DATA__: GlobalData;

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event: Event): void {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail

  //console.log(data.args)
  const fig: string = data.args["fig"];
  const height: number = data.args["height"];
  const width: number = data.args["width"];

  function onMapClick(e: any) {
    const global_data = __GLOBAL_DATA__;
    global_data.lat_lng_clicked = e.latlng;
    debouncedUpdateComponentValue()
  }

  let debouncedUpdateComponentValue = debounce(updateComponentValue, 250)

  function updateComponentValue() {
    const global_data = __GLOBAL_DATA__;
    let map = global_data.map;
    let bounds = map.getBounds();
    Streamlit.setComponentValue({
      last_clicked: global_data.lat_lng_clicked,
      last_object_clicked: global_data.last_object_clicked,
      all_drawings: global_data.all_drawings,
      last_active_drawing: global_data.last_active_drawing,
      bounds: bounds,
    })
  }

  function onMapMove(e: any) {
    debouncedUpdateComponentValue()
  }

  function onDraw(e: any) {
    return onLayerClick(e);
  }

  function onLayerClick(e: any) {
    const global_data = __GLOBAL_DATA__;
    global_data.last_object_clicked = e.latlng;
    if (e.layer.toGeoJSON) {
      global_data.last_active_drawing = e.layer.toGeoJSON();
    }
    if (e.target._layers) {
      let details = []
      let layers = e.target._layers;
      for (let key in layers) {
        let layer = layers[key];
        if (layer.toGeoJSON) {
          details.push(layer.toGeoJSON());
        }
      }
      global_data.all_drawings = details;
    }
    debouncedUpdateComponentValue()
  }

  if (map == null) {
    try {
      map = __GLOBAL_DATA__.map;
    } catch (e) {
      // Only run this if the map hasn't already been created (and thus the global
      //data hasn't been initialized)
      const map_div = document.getElementById("map_div");
      const map_div2 = document.getElementById("map_div2");
      if (map_div2) {
        map_div2.style.height = `${height}px`
        map_div2.style.width = `${width}px`
      }
      if (map_div) {
        map_div.style.height = `${height}px`
        map_div.style.width = `${width}px`

        const render_script = document.createElement("script")
        // HACK -- update the folium-generated JS to add, most importantly,
        // the map to this global variable so that it can be used elsewhere
        // in the script.
        let set_global_data = `
          window.__GLOBAL_DATA__ = {
            map: map_div,
            bounds: map_div.getBounds(),
            lat_lng_clicked: null,
            last_object_clicked: null,
            all_drawings: null,
            last_active_drawing: null,
        };`;
        let replaced = fig + set_global_data;
        render_script.innerHTML = replaced;
        document.body.appendChild(render_script);

        const global_data = __GLOBAL_DATA__;
        let map = global_data.map;

        map.on('click', onMapClick);
        map.on('moveend', onMapMove);
        for (let key in map._layers) {
          let layer = map._layers[key];
          layer.on("click", onLayerClick)
        }
        debugger;
        map.on('draw:created', onDraw);
        //map.on('draw:edited', onDraw);

        Streamlit.setFrameHeight()
        updateComponentValue();
      }
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