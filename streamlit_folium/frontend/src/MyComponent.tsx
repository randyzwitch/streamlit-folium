import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import React, { useEffect, ReactNode } from "react"
import InnerHTML from 'dangerously-set-html-content'

//import * as L from "leaflet"

interface ReturnData {
  bbox: number[];  //start by always returning the bounding box shown
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class MyComponent extends StreamlitComponentBase<ReturnData> {
  //public state = { bbox: [34.454, -57.876] }
  public state = { bbox: [0, 0] }

  //public componentDidMount = (): void => {
  //  const fig: string = this.props.args["fig"]
  //window.eval(fig);
  //}
  public componentDidUpdate = (): void => {
    // After we're updated, tell Streamlit that our height may have changed.
    Streamlit.setFrameHeight(500);
  }


  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible via `this.props.args`
    const fig: string = this.props.args["fig"]
    const top_id: string = this.props.args["id"]
    //console.log(fig)

    function createMarkup() {
      return {
        __html: JSON.stringify(fig)
      }
    }

    const script = `<script>${fig}</script>`;

    //useEffect(() => Streamlit.setFrameHeight());
    //Streamlit.setFrameHeight(500);

    return (
      <div style={{ border: "1px solid black" }}>
        <div id={top_id}></div>
        <InnerHTML html={script} />
      </div >
    )

    /*
        <script
          dangerouslySetInnerHTML={{ __html: `${fig}` }}
        />
    */

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