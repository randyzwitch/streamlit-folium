import { Streamlit, RenderData } from "streamlit-component-lib"
import * as L from "leaflet"
//import { render } from "@testing-library/react"

let map: any = null;

type InitialData = {
  map: any;
};

declare var __INITIAL_DATA__: InitialData;

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

  console.log(data.args)
  const fig: string = data.args["fig"];
  const top_id: string = data.args["id"];
  const height: number = data.args["height"];
  const width: number = data.args["width"];
  const map_details: { [key: string]: string } = data.args["map_details"];

  let crs_lookup: { [key: string]: any } = {
    "EPSG3857": L.CRS.EPSG3857,
    "EPSG3395": L.CRS.EPSG3395,
    "Earth": L.CRS.Earth,
    "EPSG4326": L.CRS.EPSG4326,
    "Simple": L.CRS.Simple,
  }

  map_details["crs"] = crs_lookup[map_details["crs"]] || L.CRS.EPSG3857;

  //Streamlit.setComponentValue(3);

  function onMapClick(e: any) {
    //console.log(Streamlit);
    //console.log(Streamlit.setComponentValue);
    Streamlit.setComponentValue(e.latlng);
  }

  if (map == null) {
    try {
      map = __INITIAL_DATA__.map;
    } catch (e) {
      const map_div = document.getElementById("map_div");
      if (map_div) {
        map_div.style.height = `${height}px`
        map_div.style.width = `${width}px`
        //map_div.setAttribute("id", top_id)
        document.body.appendChild(map_div)

        //map = L.map("map_div", map_details);

        const render_script = document.createElement("script")
        //let replaced = fig.split(top_id).join("map");
        let replaced = fig + `\nwindow.__INITIAL_DATA__ = {map: map_div};`;
        render_script.innerHTML = replaced;
        document.body.appendChild(render_script);

        const initial_data = __INITIAL_DATA__;
        let map = initial_data.map;

        map.on('click', onMapClick)
      }
    }
  }

  // We tell Streamlit to update our frameHeight after each render event, in
  // case it has changed. (This isn't strictly necessary for the example
  // because our height stays fixed, but this is a low-cost function, so
  // there's no harm in doing it redundantly.)
  //Streamlit.setFrameHeight(height + 10)
}

// Attach our `onRender` handler to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

//Streamlit.setComponentValue(3);

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight(500)