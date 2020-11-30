import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import React, { ReactNode } from "react"

interface ReturnData {
  bbox: number[];  //start by always returning the bounding box shown
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class MyComponent extends StreamlitComponentBase<ReturnData> {
  //public state = { bbox: [34.454, -57.876] }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible via `this.props.args`
    const fig: string = this.props.args["fig"]
    console.log(fig)

    function createMarkup() {
      return {
        __html: atob(fig)
      }
    }

    return (
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
      <div dangerouslySetInnerHTML={createMarkup()} />
    )
  }

}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)
