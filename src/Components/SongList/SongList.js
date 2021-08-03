import Song from '../Song/Song.js'
import React, { Component } from "react"
import "./SongList.css"


class SongList extends Component{

    constructor(props){
        super(props);
      }
    
    render() {
        return (<div>      
        {this.props.songs.map((song,index)=>{
            return <Song title = {song.title} 
            lines = {song.lines} 
            key ={"song" + index} 
            isHide={song.visible}
            song = {index}
            changeSongVisibility = {this.props.changeSongVisibility}
            toggleLine = {this.props.toggleLine}
            />
        })}
            </div>
        );  
      }

 



}

export default SongList