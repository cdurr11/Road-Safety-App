import React from 'react';
import "./css/map.css";
import {Map, Marker, TileLayer, Popup, Viewport, LatLng, Polyline, GeoJSON} from "react-leaflet";
import {LatLngExpression, latLng} from "leaflet";
import {connect} from 'react-redux';
import {addPolyline} from "./redux/actions";
// @ts-ignore
// import chicago from './chicago2.json';
// import chicago from './basic.json'

interface LeafletMapProps {
  addPolyline: any,
    polyLines: any,
}
const ADD_POLYLINE_POINT = 'ADD_POLYLINE_POINT';

interface LeafletMapsState {
    drawingPolyline: boolean;
    polyLinePoints: number[][];
    zoom: number;
    latitude: number;
        longitude: number;
}

class LeafletMap extends React.Component<LeafletMapProps, LeafletMapsState> {
    map: any;

    state = {
        drawingPolyline: false,
        polyLinePoints: [],
        zoom: 13,
        latitude: 41.8781,
        longitude: -87.6298,
    };

    handleAddPolyline = (e: any) => {
      const clickedPoint: number[] = [e.latlng.lat, e.latlng.lng];
      this.props.addPolyline(clickedPoint);
    };

    handleMove(e: any) {
        this.setState({
                        zoom: e.target._zoom, 
                        latitude: e.target.getCenter().lat,
                        longitude: e.target.getCenter().lng
                    });
    }

    fetchJSON(url: string) {
        return fetch(url, {
            headers : { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
           }}).then(function(response) {
            console.log(response);
            return response.json();
          });
    }

    componentWillMount() {
        // this.setState({data: chicago});
        // console.log(chicago);
        // var newData = this.fetchJSON("src/chicago.geojson").then(() => {console.log("2")});
        // var newData = this.fetchJSON("./src/chicago.geojson").then((newData) => {this.setState({data:newData})});
        // var newData = this.fetchJSON("./src/chicago.json").then((newData) => {this.setState({data:newData})});
        // this.setState({data: newData});
        // this.setState({data: this.fetchJSON("road-safety-ui/src/Street Center Lines (1).geojson")});
    }

    render() {
        // console.log("data", this.state.data.data);
        let view : Viewport = {center: [this.state.latitude, this.state.longitude], zoom: this.state.zoom };
        return (
            <div>
                <div className="leaflet-map-container">
                    <Map onMove={(e: any) => this.handleMove(e)} ref={(ref) => { this.map = ref; }} viewport={view} onClick={(e: any) => this.handleAddPolyline(e)}>
                        <TileLayer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
                        />
                        <Polyline positions={this.props.polyLines}/>
                        {/*
                            // @ts-ignore */}
                        {/* <GeoJSON key={"geojson"} data={chicago}/> */}
                    </Map>
                </div>
            </div>
        );
    }
}

const mapStateToProps = (state: any) => {
    return { polyLines: state.polyLines };
};
export default connect(mapStateToProps, { addPolyline })(LeafletMap);
