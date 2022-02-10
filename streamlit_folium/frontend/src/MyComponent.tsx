import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import React, { ReactNode } from "react"
import InnerHTML from 'dangerously-set-html-content'
import * as L from "leaflet"
interface ReturnData {
  bbox: number[];  //start by always returning the bounding box shown
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */

class MyComponent extends StreamlitComponentBase<ReturnData> {
  public state = { bbox: [0, 0] }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible via `this.props.args`
    const fig: string = this.props.args["fig"];
    const top_id: string = this.props.args["id"];
    const height: number = this.props.args["height"];
    const width: number = this.props.args["width"];
    const map_details: any = this.props.args["map_details"];
    return

    //map_details["crs"] = L.CRS[map_details["crs"]];
    /*const map_div = document.createElement("div")
    map_div.style.height = `${height}px`
    map_div.style.width = `${width}px`
    map_div.setAttribute("id", top_id)
    document.body.appendChild(map_div)
    */
    // TODO: Handle generic Figure

    //const placeholder = (
    //  <div id={top_id} style={{ height: height, width: width }} />
    //)
    //const mymap = L.map(placeholder.props.id, map_details);
    //const mymap = L.map("map_id", map_details);
    //const updated = fig.replaceAll(top_id, "mymap");
    //console.log(updated);
    //const script = `<script>${updated}</script>`;
    const c = fig.split("var ").join("");
    const script = `<script>${c}</script>`;

    function onMapClick(e: any) {
      /*L.popup()
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(mymap)
      */
      Streamlit.setComponentValue(e.latlng)
      Streamlit.setFrameHeight()
    }
    //mymap.on("click", onMapClick)

    //<div id={top_id} style={{ height: height, width: width }}></div>

    //return (<div> </div>)

    return (
      <div>
        <h1>Hi</h1>
        <InnerHTML html={script} />
      </div >
    )

    return (
      <script>
        {fig}
      </script>
      // <div style={{ width: "100%" }}>
      //   <div style={{ position: "relative", width: "100%", height: 0, paddingBottom: "60%" }}>
      //     <iframe
      //       title="hello"
      //       src="about:blank"
      //       style={{
      //         position: "absolute",
      //         width: "100%",
      //         height: "100%",
      //         left: 0,
      //         top: 0,
      //         border: "none !important"
      //       }}
      //       data-html={fig}
      //       allowFullScreen
      //       onLoad="this.contentDocument.open();this.contentDocument.write(atob(this.getAttribute('data-html')));this.contentDocument.close();"
      //     ></iframe>
      //   </div>
      // </div>
      //<div dangerouslySetInnerHTML={createMarkup()} />
      //<div dangerouslySetInnerHTML={{ "__html": fig }} />
    )
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)