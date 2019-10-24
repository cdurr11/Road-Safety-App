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
}

class LeafletMap extends React.Component<LeafletMapProps, LeafletMapsState> {

    state = {
        drawingPolyline: false,
        polyLinePoints: [],
    };

    handleAddPolyline = (e: any) => {
      const clickedPoint: number[] = [e.latlng.lat, e.latlng.lng];
      this.props.addPolyline(clickedPoint);
    };

    render() {
        let view : Viewport = {center: [37.7749, -122.4194], zoom: null };
        return (
            <div>
                <div className="leaflet-map-container">
                    <Map viewport={view} zoom={13} onClick={(e: any) => this.handleAddPolyline(e)}>
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
