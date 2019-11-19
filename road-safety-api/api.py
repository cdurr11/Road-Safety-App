import requests
from flask import Flask
from flask import request
import json
import flask
from flask_cors import CORS
from API_KEY import api_key, weather_api_key
from weather_constants import weather_const_map

app = Flask(__name__)
CORS(app)


def generate_path_request(points):
    path_string = ""
    for point_i in range(len(points)):
        path_string = path_string + str(points[point_i][0]) + "," + str(points[point_i][1])
        if point_i != len(points) - 1:
            path_string += "|"
    
    return path_string
        
def extract_roads(roads_api_response):
    place_ids = set([])
    cities = set([])
    for point in roads_api_response:
        current_placeId = point['placeId']
        if current_placeId not in place_ids:
            place_ids.add(current_placeId)
    roads = set([])
    for placeId in place_ids:
        place_query = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+placeId+"&fields=name,rating,formatted_phone_number&key="+api_key
        place = requests.get(place_query).content
        place_json = json.loads(place)
        print(place_json)
        try:
            road_name = place_json['result']['name']
        except:
            pass

        if road_name not in roads:
            roads.add(road_name)
    return roads

#returns a 2D list of points
def process_points(points):
    final_points_arr = []
    for i in range(0, (len(points) // 100) + 1, 100):
        final_points_arr.append(points[i:min(len(points), i + 100)])
    
    # print(final_points_arr)
    return final_points_arr

def fetch_interpolated_points(subdivided_points):
    all_points = []
    for point_arr in subdivided_points:
        path_string = generate_path_request(point_arr)
        response_roads = requests.get('https://roads.googleapis.com/v1/snapToRoads?path='+path_string+'&interpolate=true&key='+api_key).content
        locations = json.loads(response_roads)['snappedPoints']
        all_points.extend(locations)

    return all_points

def get_weather(interpolated_points):
    final_weather = []
    for point_i in range(0, len(interpolated_points), 50):
        latitude = str(interpolated_points[point_i]["location"]["latitude"])
        longitude = str(interpolated_points[point_i]["location"]["longitude"])
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+latitude+"&lon="+longitude+"&APPID="+weather_api_key).content
        
        weather_id = json.loads(response)['weather'][0]['id']
        weather_type = weather_const_map[weather_id // 100]
        final_weather.append(latitude, longitude, weather_type)
    
    return final_weather

@app.route('/analyze-route', methods=['GET', 'POST'])
def analyze_route():
    data = request.json
    points =  data['points']

    subdivided_points = process_points(points)
    interpolated_points = fetch_interpolated_points(subdivided_points)
    roads = extract_roads(interpolated_points)
    route_weather = get_weather(interpolated_points)
    response = {"snappedPoints": interpolated_points}
    return response

if __name__ == "__main__":
    app.run()