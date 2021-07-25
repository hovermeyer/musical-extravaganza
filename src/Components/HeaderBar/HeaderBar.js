import React, { Component } from "react"
import "./HeaderBar.css"


class HeaderBar extends Component{

    constructor(props) {
        super(props);
        this.handleTermChange = this.handleTermChange.bind(this)
     }

    render() {
        return (<div >
            <h1>
              Hamilton Lyric Extravaganza (Currently Featuring Songs from Joseph)
            </h1>
            <input onChange = {this.handleTermChange} value={this.props.searchValue}/>
            <h2>Statistics</h2>
            <h3>Unique Words :{this.props.uniqueFound} / {this.props.uniqueTotal} ( {Math.round(this.props.uniqueFound/this.props.uniqueTotal *100*100)/100} %)</h3>
            <h3>All Words :{this.props.allFound} / {this.props.allTotal} ( {Math.round(this.props.allFound/this.props.allTotal *100*100)/100} %)</h3>
            </div>
        );  
      }
      handleTermChange(e){
          this.props.handleTermChange(e)
      }


}

export default HeaderBar