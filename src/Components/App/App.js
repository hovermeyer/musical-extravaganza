import React, { Component } from "react"

import "./App.css"

import SongList from '../SongList/SongList.js'

import HeaderBar from '../HeaderBar/HeaderBar.js'

class App extends Component{

    constructor(props) {
        super(props);
        //const data = require('../../Utils/TestInputFile.json');
        const data = require('../../Utils/joseph_v2.json');

        let songDetails = data.SongDetails

        let totalWords = 0 
        songDetails.forEach( song=>{
          song["visible"] = true
          song.lines.forEach(line =>
            {
              line.peek=false
              totalWords += line.words.length
              line.knownWords = line.words.map(word => null)
            })
          })
          this.handleTermChange = this.handleTermChange.bind(this)
          this.checkWords= this.checkWords.bind(this)
          this.changeSongVisibility = this.changeSongVisibility.bind(this)
          this.toggleLine = this.toggleLine.bind(this)

        
    
        this.state = {songDetails : songDetails,
          wordDetails: data["WordDetails"],
          searchValue:"",
          wordsFound:{},
          totalWords:totalWords,
          foundCount:0
        }


      }

    render() {
      return (
        <div className="App">
          <div className="hero">
            <HeaderBar 
              searchValue={this.state.searchValue} 
              handleTermChange={this.handleTermChange}
              uniqueTotal={Object.keys(this.state.wordDetails).length}
              uniqueFound={Object.keys(this.state.wordsFound).length}
              allTotal={this.state.totalWords}
              allFound={this.state.foundCount}

            />
            </div>
            <div className="content">
            <SongList 
              songs={this.state.songDetails}
              changeSongVisibility={this.changeSongVisibility}
              toggleLine = {this.toggleLine}
            />
            </div>
        </div>
      );

      }


           //Purpose: set search term based on change event passed
  handleTermChange(e){
    console.log("handling Change")
    let currentState=this.state
    currentState.searchValue = e.target.value
    let indexesToChange = this.checkWords(currentState.searchValue)
    console.log(indexesToChange)
    if (indexesToChange != null ){
    indexesToChange.forEach(wordLocator=>{
      let song = wordLocator[0]
      let line = wordLocator[1]
      let word = wordLocator[2]
      //console.log(song + " " + word + " " + line)
      
      currentState.songDetails[song].lines[line].knownWords[word] = currentState.songDetails[song].lines[line].words[word] 
      })
      currentState.wordsFound[currentState.searchValue] = "Found"
      currentState.searchValue=""
      console.log(currentState.wordsFound)
      currentState.foundCount +=indexesToChange.length
    }

  this.setState(currentState)

  }

  checkWords(e){
    console.log("Checking" + this.state.wordsFound[e])
    //this.state.wordsFound.forEach(word=>console.log(word))
      if(!this.state.wordsFound[e]){
        console.log("returning indexes")
        return this.state.wordDetails[e]
      }else{
        console.log("returning null")
        return null
      }
  }

  toggleLine(lineNumber,songNumber){
    let currentSongDetails= this.state.songDetails;
    currentSongDetails[songNumber].lines[lineNumber].peek = !currentSongDetails[songNumber].lines[lineNumber].peek
    this.setState({songDetails:currentSongDetails})
  }

  //Purpose: add a track to the playlist
  changeSongVisibility(song){
    var currentSongDetails = this.state.songDetails
    currentSongDetails[song].visible=!currentSongDetails[song].visible

     this.setState({songDetails: currentSongDetails})
   }
 

}

export default App