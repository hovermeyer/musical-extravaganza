import React, { Component } from "react"
import Line from '../Line/Line.js'
import './Song.css'


class Song extends Component{

    constructor(props) {
        super(props);
        this.renderAction = this.renderAction.bind(this)
        this.changeSongVisibility = this.changeSongVisibility.bind(this)
        this.renderLines = this.renderLines.bind(this)
      }

    render() {
        return (<div> 
            <h2 className='SongTitle'>{this.props.title} ({this.calculateCompleted()}) <a>{this.renderAction()}</a></h2>
            {this.renderLines()}
                </div>
            );  
    }

    calculateCompleted(){
        var totalWords = 0
        var totalKnownWords = 0
        this.props.lines.forEach(line=>{
            totalWords += line.words.length
            totalKnownWords += line.knownWords.filter(x=>x!=null).length
        })

        return totalKnownWords + "/" + totalWords + " " + Math.round(totalKnownWords/totalWords*100*100)/100 +"%"

        
    }

    renderAction(){
        if (this.props.isHide){
          return <a onClick ={this.changeSongVisibility}>-</a>
        }else{
          return <a onClick ={this.changeSongVisibility} >+</a>
        }
      }

    renderLines(){
        if(this.props.isHide){
            return             (<div> {this.props.lines.map((line,index)=>{   
                return <Line 
                    line = {index}
                    song={this.props.song}
                    words = {line.words} 
                    knownWords = {line.knownWords}
                    speaker= {line.speaker} 
                    format={line.format} 
                    startOfSection = {line["start-of-section"]}
                    peek ={line.peek} 
                    toggleLine = {this.props.toggleLine}/>
            })}</div>)

        }else{
            return null
        }
    }

    replaceBlank(word){
        if (word==null){
            return "___"    
        }else{
            return word
        }
      }

      changeSongVisibility(){
          this.props.changeSongVisibility(this.props.song)

      }

}

export default Song