import React, { Component } from "react"
import Line from '../Line/Line.js'
import ProgressBar from '../ProgressBar/ProgressBar.js'
import './Song.css'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCaretDown, faCaretUp } from '@fortawesome/free-solid-svg-icons'

class Song extends Component {

  constructor(props) {
    super(props);
    this.renderAction = this.renderAction.bind(this)
    this.changeSongVisibility = this.changeSongVisibility.bind(this)
    this.renderLines = this.renderLines.bind(this)
  }

  render() {
    return (
      <div className="song">
        <div className="song-header">
          <a onClick={this.changeSongVisibility}><h2 className="song-title">{this.props.title}</h2></a>
          {this.renderAction()}
          <div className="song-progress">
            <ProgressBar count={this.props.foundWords} total={this.props.totalWords} />
          </div>
        </div>
        {this.renderLines()}
      </div>
    );
  }

  renderAction() {
    if (this.props.isHide) {
      // return <a onClick={this.changeSongVisibility}>-</a>
      return <a className="song-collapse" onClick={this.changeSongVisibility}><FontAwesomeIcon icon={faCaretDown} /></a>
    } else {
      return <a className="song-collapse" onClick={this.changeSongVisibility} ><FontAwesomeIcon icon={faCaretUp} /></a>
    }
  }

  renderLines() {
    if (this.props.isHide) {
      return (<div className="song-lines"> {this.props.lines.map((line, index) => {
        return <Line
          line={index}
          key={index}
          song={this.props.song}
          words={line.words}
          knownWords={line.knownWords}
          speaker={line.speaker}
          format={line.format}
          startOfSection={line["start-of-section"]}
          peek={line.peek}
          toggleLine={this.props.toggleLine} />
      })}</div>)

    } else {
      return null
    }
  }

  replaceBlank(word) {
    if (word == null) {
      return "___"
    } else {
      return word
    }
  }

  changeSongVisibility() {
    this.props.changeSongVisibility(this.props.song)

  }
}

export default Song
