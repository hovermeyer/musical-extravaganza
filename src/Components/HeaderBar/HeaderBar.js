import React, { Component } from "react"
import "./HeaderBar.css"
import ProgressBar from '../ProgressBar/ProgressBar.js'
import DataTable from 'react-data-table-component'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faDownload, faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'

class HeaderBar extends Component {
  constructor(props) {
    super(props);
    this.handleTermChange = this.handleTermChange.bind(this)
    this.expandAllSongs = this.expandAllSongs.bind(this)
    this.collapseAllSongs = this.collapseAllSongs.bind(this)
    this.renderLog = this.renderLog.bind(this)
    this.downloadSaveFile = this.downloadSaveFile.bind(this)
    this.onFileUpload = this.onFileUpload.bind(this)
  }

  render() {
    return (
      <div className="header-bar">
        <h1>
          Hamilton Lyric Extravaganza
        </h1>
        <input placeholder="type here" onChange={this.handleTermChange} value={this.props.searchValue} /> &nbsp; &nbsp;
        <div className="collapse-button-bar">
          <a className="collapse-all-button" onClick={this.expandAllSongs}><FontAwesomeIcon icon={faPlus} /> Expand all</a>
          <a className="collapse-all-button" onClick={this.collapseAllSongs}><FontAwesomeIcon icon={faMinus} /> Collapse all</a>
        </div>
        <h2>Statistics</h2>
        <div className="stats-line">
          <h3>Unique Words:</h3>
          <div className="overall-progress">
            <ProgressBar count={this.props.uniqueFound} total={this.props.uniqueTotal} />
          </div>
        </div>
        <div className="stats-line">
          <h3>All Words:</h3>
          <div className="overall-progress">
            <ProgressBar count={this.props.allFound} total={this.props.allTotal} />
          </div>
        </div>
        <h3>Log:</h3>
        {this.renderLog()}
        <div className="download-button">
          <a onClick={this.downloadSaveFile}>Download <FontAwesomeIcon icon={faDownload} /></a>
        </div>
        <div className='upload-button'>
          <input type="file" name="file" onChange={this.onFileUpload}/>
        </div>
      </div>
    );
  }

  renderLog() {
    const columns = [
      {
        name: 'Timestamp',
        selector: row => `${row.time.getHours().toString().padStart(2, '0')}:${row.time.getMinutes().toString().padStart(2, '0')}:${row.time.getSeconds().toString().padStart(2, '0')}`,
        sortable: true,
      },
      {
        name: 'Word',
        selector: row => row.word,
        sortable: true,
      },
      {
        name: '# of instances',
        selector: row => row.instance_count,
        sortable: true,
      },
    ];

    return <DataTable
      columns={columns}
      data={this.props.log}
      striped={true}
      noDataComponent="No words found yet"
      fixedHeader={true}
      fixedHeaderScrollHeight="20vh"
    />
  }

  formatLog(log) {
    return (log.map((logEntry) => {
      return {
        time: logEntry.time,
        word: logEntry.word,
      }
    }));
  }

  onFileUpload(e){
    this.props.loadLog(e.target.files[0])
  }

  downloadSaveFile() {
    const element = document.createElement("a");
    const file = new Blob([JSON.stringify(this.formatLog(this.props.log))],
      { type: 'text/plain;charset=utf-8' });
    element.href = URL.createObjectURL(file);
    element.download = `${new Date().toISOString()}.log.json`;
    document.body.appendChild(element);
    element.click();
  }

  handleTermChange(e) {
    this.props.handleTermChange(e)
  }

  expandAllSongs() {
    this.props.expandAllSongs()
  }

  collapseAllSongs() {
    this.props.collapseAllSongs()
  }
}

export default HeaderBar
