import React from 'react';
import './css/app.css';
import LeafletMap from "./map.component";
import {connect} from 'react-redux';
import {clearPolyline, addSnappedPolyline} from "./redux/actions";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.snapPolyline = this.snapPolyline.bind(this);
    }

  processPoints(points) {
    if (points.length > 0) {
      let finalPoints = [];
      points.forEach(point => {
        finalPoints.push([point.location.latitude, point.location.longitude]);
      });
      this.props.addSnappedPolyline(finalPoints);
    }
  }

  snapPolyline() {
      const lineData = {points: this.props.polyLines};
      fetch('http://localhost:5000/analyze-route', {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }, 
          method: 'POST',
          body: JSON.stringify(lineData)
      })
          .then(response => response.json())
          .then(data => {this.processPoints(data.snappedPoints); console.log(data); 
            alert("Our model predicted a crash on " + data.value[0] + " out of " + data.value[1] + " points along your route")});
  }

  render() {
      return (
        <div className="App">
              <div className='top-bar'/>
              <div className='content-container'>
                  <div className='side-bar'>
                      <button onClick={this.snapPolyline}>Map</button>
                      <button onClick={this.props.clearPolyline}>Clear</button>
                  </div>
                  <LeafletMap getPolyLine={this.getPolyline}/>
              </div>
          </div>
      );
  }
}

const mapDispatchToProps = dispatch => {
  return {
    clearPolyline,
    addSnappedPolyline,
  }
}

const mapStateToProps = (state) => {
    return { polyLines: state.polyLines };
};

export default connect(mapStateToProps, {clearPolyline, addSnappedPolyline})(App);
