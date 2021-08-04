import React, { Component } from "react"
import "./HeaderBar.css"

class HeaderBar extends Component {
  constructor(props) {
    super(props);
    this.handleTermChange = this.handleTermChange.bind(this)
    this.renderLog = this.renderLog.bind(this)
  }

  render() {
    return (<div >
      <h1>
        Hamilton Lyric Extravaganza
      </h1>
      <input onChange={this.handleTermChange} value={this.props.searchValue} /> &nbsp; &nbsp;
      <h2>Statistics</h2>
      <h3>Unique Words: {this.props.uniqueFound} / {this.props.uniqueTotal} ( {Math.round(this.props.uniqueFound / this.props.uniqueTotal * 100 * 100) / 100} %)</h3>
      <h3>All Words: {this.props.allFound} / {this.props.allTotal} ( {Math.round(this.props.allFound / this.props.allTotal * 100 * 100) / 100} %)</h3>
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
