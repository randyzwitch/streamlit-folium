import { Streamlit, RenderData } from "streamlit-component-lib"
import * as L from "leaflet"
import { updateContinue } from "typescript";
import { debug } from "console";
//import { render } from "@testing-library/react"

let map: any = null;

type GlobalData = {
  map: any;
  lat_lng_clicked: any;
  last_object_clicked: any;
  bounds: any;
};

declare var __GLOBAL_DATA__: GlobalData;

//console.log("SET INITIAL DATA");
//console.log(window.__INITIAL_DATA__);

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
  const top_id: string = data.args["id"];
  const height: number = data.args["height"];
  const width: number = data.args["width"];
  /*const map_details: { [key: string]: string } = data.args["map_details"];

  let crs_lookup: { [key: string]: any } = {
    "EPSG3857": L.CRS.EPSG3857,
    "EPSG3395": L.CRS.EPSG3395,
    "Earth": L.CRS.Earth,
    "EPSG4326": L.CRS.EPSG4326,
    "Simple": L.CRS.Simple,
  }

  map_details["crs"] = crs_lookup[map_details["crs"]] || L.CRS.EPSG3857;
  */

  //Streamlit.setComponentValue(3);

  function onMapClick(e: any) {
    const global_data = __GLOBAL_DATA__;
    global_data.lat_lng_clicked = e.latlng;
    updateComponentValue()
  }

  function updateComponentValue() {
    const global_data = __GLOBAL_DATA__;
    let map = global_data.map;
    let bounds = map.getBounds();
    Streamlit.setComponentValue({
      last_clicked: global_data.lat_lng_clicked,
      last_object_clicked: global_data.last_object_clicked,
      bounds: bounds,
    })
  }

  function onMapMove(e: any) {
    updateComponentValue()
  }

  function onLayerClick(e: any) {
    const global_data = __GLOBAL_DATA__;
    global_data.last_object_clicked = e.latlng;
    updateComponentValue()
  }

  if (map == null) {
    try {
      map = __GLOBAL_DATA__.map;
    } catch (e) {
      debugger;
      // Only run this if the map hasn't already been created (and thus the global
      //data hasn't been initialized)
      const map_div = document.getElementById("map_div");
      if (map_div) {
        map_div.style.height = `${height}px`
        map_div.style.width = `${width}px`
        //document.body.appendChild(map_div);

        const render_script = document.createElement("script")
        // HACK -- there must be a better way
        let set_global_data = `
          window.__GLOBAL_DATA__ = {
            map: map_div,
            bounds: map_div.getBounds(),
            lat_lng_clicked: null,
            last_object_clicked: null,
        };`;
        let replaced = fig + set_global_data;
        render_script.innerHTML = replaced;
        document.body.appendChild(render_script);

        const global_data = __GLOBAL_DATA__;
        let map = global_data.map;

        map.on('click', onMapClick);
        map.on('zoomend', onMapMove);
        map.on('moveend', onMapMove);
        for (let key in map._layers) {
          let layer = map._layers[key];
          layer.on("click", onLayerClick)
        }
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

//Streamlit.setComponentValue(3);

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()