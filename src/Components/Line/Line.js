import React, { Component } from "react"
import "./Line.css"


class Line extends Component{

    constructor(props) {
        super(props);
        this.getLine= this.getLine.bind(this);
        this.getSpeakerLabel= this.getSpeakerLabel.bind(this);
        this.onDoubleClick =this.onDoubleClick.bind(this);
        this.toggleLine = this.toggleLine.bind(this);
        this.renderPeek = this.renderPeek.bind(this);


      }

    render() {
        return (<div>
          <p >{this.getSpeakerLabel()} {this.getLine(this.props.format, this.props.knownWords)} 
          <a onClick={this.toggleLine}>{this.renderPeek()}</a></p>
          </div> 
        );    
      }

    getSpeakerLabel(){
      if (this.props.startOfSection){
        return <p>{this.props.speaker}:</p>
      } 
    }

    toggleLine(){
      this.props.toggleLine(this.props.line, this.props.song)
    }

    renderPeek(){
      if (this.props.peek){
        return "(" +this.getLine(this.props.format, this.props.words)+")"
      }else{
        return "+"
      }
    }

    getLine(formattedString, knownWords){
      knownWords.forEach( (word,index)=> {
        formattedString=formattedString.replace("{"+ index +"}",this.replaceBlank(word))
      })
      return formattedString
    }

    onDoubleClick(e){
      
      console.log(e)
    }

      
    replaceBlank(word){
      if (word==null){
          return "___"    
      }else{
          return word
      }
    }

}

export default Line