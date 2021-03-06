import React, { Component } from "react"
import "./Line.css"

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faEye } from '@fortawesome/free-solid-svg-icons'

class Line extends Component {

  constructor(props) {
    super(props);
    this.getLine = this.getLine.bind(this);
    this.getSpeakerLabel = this.getSpeakerLabel.bind(this);
    this.toggleLine = this.toggleLine.bind(this);
    this.renderPeek = this.renderPeek.bind(this);
  }

  render() {
    return (<div>
      {this.getSpeakerLabel()}<p> {this.getLine(this.props.format, this.props.knownWords)} &nbsp; &nbsp;
        <a onClick={this.toggleLine}>{this.renderPeek()}</a></p>
    </div>
    );
  }

  getSpeakerLabel() {
    if (this.props.startOfSection) {
      return <p className="speaker-label">{this.props.speaker}:</p>
    }
  }

  toggleLine() {
    this.props.toggleLine(this.props.line, this.props.song)
  }

  renderPeek() {
    if (this.props.peek) {
      return "(" + this.getLine(this.props.format, this.props.words) + ")"
    } else {
      return <FontAwesomeIcon icon={faEye} />
    }
  }

  getLine(formattedString, knownWords) {
    knownWords.forEach((word, index) => {
      formattedString = formattedString.replace("{" + index + "}", this.replaceBlank(word))
    })
    return formattedString
  }


  replaceBlank(word) {
    if (word == null) {
      return "___"
    } else {
      return word
    }
  }

}

export default Line
