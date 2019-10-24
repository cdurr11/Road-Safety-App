import React from 'react';
import './css/app.css';
import LeafletMap from "./map.component";
import {connect} from 'react-redux';
import {clearPolyline} from "./redux/actions";

class App extends React.Component {

  snapPolyline() {

  }

  render() {
      return (
        <div className="App">
              <div className='top-bar'/>
              <div className='content-container'>
                  <div className='side-bar'>
                      <button onClick={this.snapPolyline()}>Map</button>
                      <button onClick={this.props.clearPolyline}>Clear</button>
                  </div>
                  <LeafletMap getPolyLine={this.getPolyline}/>
              </div>
          </div>
      );
  }
}

const mapStateToProps = state => {
    const polyLines = state.polyLines;
    return { polyLines };
};

export default connect(mapStateToProps, {clearPolyline})(App);
