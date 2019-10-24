import React from 'react';
import './css/app.css';
import LeafletMap from "./map.component";
import {connect} from 'react-redux';
import {clearPolyline} from "./redux/actions";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.snapPolyline = this.snapPolyline.bind(this);
    }



  snapPolyline() {
      const lineData = {points: this.props.polyLines};
      fetch('http://localhost:5000/', {
          method: 'post',
          body: JSON.stringify(lineData)
      })
          .then( response => response.json())
          .then(data => {console.log(data);});
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

const mapStateToProps = (state) => {
    return { polyLines: state.polyLines };
};

export default connect(mapStateToProps, {clearPolyline})(App);
