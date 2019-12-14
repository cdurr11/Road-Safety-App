import requests
from flask import Flask
from flask import request
import json
import flask
from flask_cors import CORS
from API_KEY import api_key, weather_api_key
from weather_constants import weather_const_map
import sklearn
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import datasets, linear_model
import matplotlib.pyplot as plt
from classifier import avg_temp_mean 
from classifier import avg_temp_std
from classifier import get_scaled_value

from classifier import avg_rain_mean 
from classifier import avg_rain_std

from classifier import avg_snow_mean 
from classifier import avg_snow_std

import pandas as pd

import random





import datetime
dt = datetime.datetime.now()

# from classifier import clf


# from models import db_session, alameda, san_francisco, san_mateo

app = Flask(__name__)
CORS(app)

# Working pymysql command
# print(db_session.query(alameda).filter(alameda.CASE_ID == 5414040).first().COLLISION_TIME)

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

def convert_precip_to_inches(precip_mm):
    return precip_mm * 0.0393701

def convert_to_fahrenheit(temp_kelvin):
    return ((temp_kelvin - 273.15)* (9 / 5)) + 5

def get_weather(interpolated_points):
    final_weather = []
    for point_i in range(0, len(interpolated_points)):
        latitude = str(interpolated_points[point_i]["location"]["latitude"])
        longitude = str(interpolated_points[point_i]["location"]["longitude"])
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+latitude+"&lon="+longitude+"&APPID="+weather_api_key).content
        print("RESPONSE:", json.loads(response))
        weather_id = json.loads(response)['weather'][0]['id']
        temp = int(json.loads(response)['main']['temp'])
        rain = 0
        snow = 0
        try:
            rain = int(json.loads(response)['rain']['3h'])
        except:
            pass
        try:
            snow = int(json.loads(response)['snow']['3h'])
        except:
            pass

        rain = convert_precip_to_inches(rain)
        snow = convert_precip_to_inches(snow)
        temp = convert_to_fahrenheit(temp)

        weather_type = weather_const_map[weather_id // 100]
        # lat, long, weather_type, rain (mm), snow(mm)
        final_weather.append((latitude, longitude, weather_type, rain, snow, temp))
    
    return final_weather

#weather is a list, hour and day are constant
def normalize_hour(hour):
    return (hour - 12)/ 12

def normalize_month(month):
    return (month - 6) / 6

def find_velocity():
    pass

def create_pandas_df(weather, month, hour):
    HOUR = 0
    MONTH = 1
    VOLUME = 2
    AVG_TEMP = 3
    PREC_WATER = 4
    PREC_SNOW = 5

    cols = ['hour', 'month', 'volume', 'Avg Temp', 'Precipitation Water Equiv', 'Snowfall']
    df_list = []
    # 'hour', 'month', 'volume', 'Avg Temp', 'Precipitation Water Equiv', 'Snowfall'
    # TODO 1 hot
    for element in weather:
        current_list = []
        current_list.append(normalize_hour(hour))
        current_list.append(normalize_month(month))
        # TODO normalize
        current_list.append(10000)
        current_list.append(get_scaled_value(element[5], avg_temp_mean.iloc[0], avg_temp_std.iloc[0]))
        current_list.append(get_scaled_value(element[3], avg_rain_mean.iloc[0], avg_rain_std.iloc[0]))
        current_list.append(get_scaled_value(element[4], avg_snow_mean.iloc[0], avg_snow_std.iloc[0]))
        df_list.append(current_list)

    print(df_list)
    
    return pd.DataFrame(data = df_list, columns=cols)


@app.route('/analyze-route', methods=['GET', 'POST'])
def analyze_route():
    data = request.json
    points =  data['points']

    month = dt.month
    hour = dt.hour
    val = random.choice([0,0,0,1])
    subdivided_points = process_points(points)
    interpolated_points = fetch_interpolated_points(subdivided_points)
    roads = extract_roads(interpolated_points)
    route_weather = get_weather(interpolated_points)
    # print(interpolated_points)
    # print(route_weather)
    current_df = create_pandas_df(route_weather, month, hour)

    print(current_df)
    response = {"snappedPoints": interpolated_points, "value":[val, len(interpolated_points)]}
    return response

if __name__ == "__main__":
    app.run()