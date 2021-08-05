import React, { Component } from "react"
import "./App.css"

import SongList from '../SongList/SongList.js'
import HeaderBar from '../HeaderBar/HeaderBar.js'

class App extends Component {

  constructor(props) {
    super(props);
    //const data = require('../../Utils/TestInputFile.json');
    //const data = require('../../Utils/joseph.json');
    const data = require('../../Utils/hamilton.json');

    let songDetails = data.SongDetails

    let totalWords = 0
    songDetails.forEach(song => {
      song["visible"] = false
      song["allWords"] = 0
      song["foundWords"] = 0
      song.lines.forEach(line => {
        line.peek = false
        totalWords += line.words.length
        song["allWords"] += line.words.length
        line["knownWords"] = line.words.map(word => null)
      })
    })
    //Set first song to be expanded
    songDetails[0].visible = true;
    this.handleTermChange = this.handleTermChange.bind(this)
    this.checkWords = this.checkWords.bind(this)
    this.changeSongVisibility = this.changeSongVisibility.bind(this)
    this.toggleLine = this.toggleLine.bind(this)
    this.saveLog = this.saveLog.bind(this)

    this.state = {
      songDetails: songDetails,
      wordDetails: data["WordDetails"],
      searchValue: "",
      wordsFound: {},
      totalWords: totalWords,
      log: [],
      foundCount: 0,
      uniqueFound: 0,
      uniqueTotal: Object.keys(data["WordDetails"]).length,
    }
  }

  render() {
    return (
      <div className="App">
        <div className="hero">
          <HeaderBar
            searchValue={this.state.searchValue}
            handleTermChange={this.handleTermChange}
            uniqueTotal={this.state.uniqueTotal}
            uniqueFound={this.state.uniqueFound}
            allTotal={this.state.totalWords}
            allFound={this.state.foundCount}
            log={this.state.log}
            savelog={this.saveLog}
          />
        </div>
        <div className="content">
          <SongList
            songs={this.state.songDetails}
            changeSongVisibility={this.changeSongVisibility}
            toggleLine={this.toggleLine}
          />
        </div>
      </div>
    );
  }

  //Purpose: set search term based on change event passed
  handleTermChange(e) {
    let currentState = this.state
    var searchValue = e.target.value
    let indexesToChange = this.checkWords(searchValue)
    if (indexesToChange != null) {
      indexesToChange.forEach(wordLocator => {
        let song = wordLocator[0]
        let line = wordLocator[1]
        let word = wordLocator[2]
        currentState.songDetails[song].lines[line].knownWords[word] = currentState.songDetails[song].lines[line].words[word]
        currentState.songDetails[song].foundWords += 1
      })
      currentState.wordsFound[searchValue] = true
      var currentTime = new Date()
      currentState.log.unshift(
        {
          time: currentTime,
          word: searchValue,
          instance_count: indexesToChange.length,
        },
      )
      currentState.foundCount += indexesToChange.length
      currentState.uniqueFound += 1
      currentState.searchValue = ""
      this.setState(currentState)
    } else {
      this.setState({ searchValue: searchValue })
    }
  }

  checkWords(e) {
    if (!this.state.wordsFound[e]) {
      return this.state.wordDetails[e]
    } else {
      return null
    }
  }

  saveLog() {
    console.log("Saving")
  }

  toggleLine(lineNumber, songNumber) {
    let currentSongDetails = this.state.songDetails;
    currentSongDetails[songNumber].lines[lineNumber].peek = !currentSongDetails[songNumber].lines[lineNumber].peek
    this.setState({ songDetails: currentSongDetails })
  }

  //Purpose: add a track to the playlist
  changeSongVisibility(song) {
    var currentSongDetails = this.state.songDetails
    currentSongDetails[song].visible = !currentSongDetails[song].visible
    this.setState({ songDetails: currentSongDetails })
  }
}

export default App
