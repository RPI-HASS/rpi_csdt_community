import React from "react"
import {observer} from "mobx-react"
import { autorun, computed, observable, action } from "mobx"

@observer
export default class AppList extends React.Component {

  render() {
    const { shots, made, x, y, num } = this.props;

    function colorPicked(shots, made)  {
      let ratio = made / shots
      if (ratio > 1.0 || ratio < 0.0) {
        return "black"
      }
      else if (ratio < 0.05) {
        return "#0602ff"
      }
      else if (ratio < 0.10) {
        return "#3835fe"
      }
      else if (ratio < 0.15) {
        return "#504dfd"
      }
      else if (ratio < 0.2) {
        return "#6c69fc"
      }
      else if (ratio < 0.25) {
        return "#8482fc"
      }
      else if (ratio < 0.3) {
        return "#8f8efc"
      }
      else if (ratio < 0.35) {
        return "#a3a2fb"
      }
      else if (ratio < 0.4) {
        return "#bebdfa"
      }
      else if (ratio < 0.45) {
        return "#dfdffa"
      }
      else if (ratio < .5) {
        return "#f9f9f9"
      }
      else if (ratio < .55) {
        return "#fadcdc"
      }
      else if (ratio < .6) {
        return "#fac1c1"
      }
      else if (ratio < .65) {
        return "#fba7a7"
      }
      else if (ratio < .7) {
        return "#fc8a8a"
      }
      else if (ratio < .75) {
        return "#fc7777"
      }
      else if (ratio < .8) {
        return "#fd6c6c"
      }
      else if (ratio < .85) {
        return "#fd4e4e"
      }
      else if (ratio < .9) {
        return "#fe3b3b"
      }
      else if (ratio < .95) {
        return "#fe2525"
      }
      else if (ratio <= 1.0) {
        return "#ff1010"
      }
      else {
        return "black"
      }
    }
    const colorP = colorPicked(shots, made)
    let textColor = "white"
    if (colorP == "black") {
      textColor = "white"
    } else {
      textColor = colorP
    }

    return (
      <div style={{
        borderRadius: "50%",
	      width: "70px",
	      height: "70px",
        backgroundColor: colorP,
        color: textColor,
        textAlign: "center",
        fontSize: "20px",
        lineHeight: "70px",
        zIndex: "100",
        position: "absolute",
        left: x,
        top: y
      }}>{num}</div>
    )
  }
}
