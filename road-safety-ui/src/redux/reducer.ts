import { ADD_POLYLINE, CLEAR_POLYLINE, ADD_SNAPPED_POLYLINE } from "./actionTypes";


const initalState = {
  polyLines: [],
};

export function polyLinesReducer(state = initalState, action: any) {
  switch (action.type) {
    case ADD_POLYLINE:
      return {...state, polyLines: [...state.polyLines, action.payload]}
    case CLEAR_POLYLINE:
      return {...state, polyLines: []};
    case ADD_SNAPPED_POLYLINE:
      return {...state, polyLines: action.payload}
    default:
      return state
  }
}