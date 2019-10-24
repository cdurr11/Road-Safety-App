import { ADD_POLYLINE, CLEAR_POLYLINE } from "./actionTypes";


const initalState = {
  polyLines: [],
};

export function polyLinesReducer(state = initalState, action: any) {
  switch (action.type) {
    case ADD_POLYLINE:
      return {...state, polyLines: [...state.polyLines, action.payload]}
    case CLEAR_POLYLINE:
      console.log("CLEARING");
      return {...state, polyLines: []};
    default:
      return state
  }
}