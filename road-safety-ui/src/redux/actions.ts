import {ADD_POLYLINE, CLEAR_POLYLINE} from "./actionTypes";

export const addPolyline = (point: number[]) => ({
  type: ADD_POLYLINE,
  payload: point
});

export const clearPolyline = (point: number[]) => ({
  type: CLEAR_POLYLINE,
});
