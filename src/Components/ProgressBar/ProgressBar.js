import React, { Component } from "react"
import './ProgressBar.css'

import { Line as Progress } from 'rc-progress';

class ProgressBar extends Component {

  // constructor(props) {
  //   super(props);
  // }

  render() {
    return (
      <div className='progress-wrapper'>
        <span className='progress-title'>{this.percent()}% ({this.props.count}/{this.props.total})</span>
        <Progress percent={this.percent()} strokeWidth="6" trailWidth="6" strokeColor="#98c964" />
      </div>
    );
  }

  percent() {
    return Math.round(this.props.count / this.props.total * 100 * 100) / 100
  }
}

export default ProgressBar
