import React, { Component } from "react"
import "./HeaderBar.css"
import ProgressBar from '../ProgressBar/ProgressBar.js'
import DataTable from 'react-data-table-component'

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


  handleTermChange(e) {
    this.props.handleTermChange(e)
  }
}

export default HeaderBar
