import React from 'react';
import "./css/map.css";
import {Map, Marker, TileLayer, Popup, Viewport, LatLng, Polyline} from "react-leaflet";
import {LatLngExpression, latLng} from "leaflet";
import {connect} from 'react-redux';
import {addPolyline} from "./redux/actions";

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
    render() {
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
