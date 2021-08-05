import React, { Component } from "react"
import "./HeaderBar.css"
import ProgressBar from '../ProgressBar/ProgressBar.js'

class HeaderBar extends Component {
  constructor(props) {
    super(props);
    this.handleTermChange = this.handleTermChange.bind(this)
    this.renderLog = this.renderLog.bind(this)
  }

  render() {
    return (
      <div className="header-bar">
        <h1>
          Hamilton Lyric Extravaganza
        </h1>
        <input placeholder="type here" onChange={this.handleTermChange} value={this.props.searchValue} /> &nbsp; &nbsp;
        <h2>Statistics</h2>
        <h3>Unique Words:</h3>
        <ProgressBar count={this.props.uniqueFound} total={this.props.uniqueTotal} />
        <h3>All Words:</h3>
        <ProgressBar count={this.props.allFound} total={this.props.allTotal} />
        <h3>Log:</h3>
        {this.renderLog()}
      </div>
    );
  }

  renderLog() {
    return (this.props.log.slice(-5,).reverse().map((logEntry, index) => {
      return (<h4 key={index}> {logEntry.timeStamp.getHours()}:{logEntry.timeStamp.getMinutes().toString().padStart(2, '0')}:{logEntry.timeStamp.getSeconds().toString().padStart(2, '0')}: You found "{logEntry.word}" which is in the show {logEntry.revealedNumber} times </h4>)
    }))
  }


  handleTermChange(e) {
    this.props.handleTermChange(e)
  }
}

export default HeaderBar
