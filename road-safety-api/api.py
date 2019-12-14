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
import pandas as pd
import random
import datetime
import re
import pickle

dt = datetime.datetime.now()

clf = pickle.load(open('../random_forest.sav', 'rb'))
street_data = pd.read_csv("../street_segments.csv", index_col=0)

app = Flask(__name__)
CORS(app)


def get_scaled_value(value, mean, std):
    return (value - mean)/ std

# Working pymysql command

def generate_path_request(points):
    path_string = ""
    for point_i in range(len(points)):
        path_string = path_string + str(points[point_i][0]) + "," + str(points[point_i][1])
        if point_i != len(points) - 1:
            path_string += "|"
    
    return path_string

def extract_roads(roads_api_response):
    place_ids = []
    for point in roads_api_response:
        current_placeId = point['placeId']
        place_ids.append(current_placeId)
    roads = []
    for placeId in place_ids:
        place_query = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+placeId+"&fields=name,rating,formatted_phone_number&key="+api_key
        place = requests.get(place_query).content
        place_json = json.loads(place)
        try:
            road_name = place_json['result']['name']
            corrected_name = re.sub(r'[0-9]', '', road_name)
            corrected_name = re.sub(r'[^\w]', '', corrected_name)
            corrected_name = re.sub(r'Ave', '', corrected_name)
            corrected_name = re.sub(r'St', '', corrected_name)
            corrected_name = re.sub(r'AVE', '', corrected_name)
            corrected_name = re.sub(r'ST', '', corrected_name)
            corrected_name = re.sub(r'DR', '', corrected_name)
            corrected_name = re.sub(r'Dr', '', corrected_name)
            corrected_name = re.sub(r'PL', '', corrected_name)
            corrected_name = re.sub(r'Pl', '', corrected_name)
            corrected_name = re.sub(r'Rd', '', corrected_name)
            corrected_name = re.sub(r'RD', '', corrected_name)
        except:
            pass

        roads.append(corrected_name)
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

def find_closest_row(latitude, longitude, road, df):

    min_dist = float('inf')
    best_row = None
    for index, row in df.iterrows():
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        dist = ((latitude - lat)**2 + (longitude - lon)**2)**(0.5)
        if dist < min_dist:
            min_dist = dist
            best_row = row

    return best_row

def one_hot_day(day):
    one_hot = []
    for i in range(7):
        if i == day:
            one_hot.append(1)
    else:
        one_hot.append(0)
    return one_hot


def make_safety_score(interpolated_points, safety_df, roads):

    safety_scores = []
    
    for point_i in range(0, len(interpolated_points), 50):
        print(type(point_i))
        latitude = float(interpolated_points[point_i]["location"]["latitude"])
        longitude = float(interpolated_points[point_i]["location"]["longitude"])
        road = roads[point_i].upper()
        print("road", road)
        print("safety_fd", safety_df['street_nam'])
        cur_df = safety_df[safety_df['street_nam'] == road]
        if cur_df.shape[0] == 0:
            continue
        row = find_closest_row(latitude, longitude, road, cur_df)
        safety_scores.append(row['safety_score'])
    
    if len(safety_scores) == 0:
        return "ERROR"
        
    return sum(safety_scores) / len(safety_scores)

    
def get_model(street_data, weather):
    max_volume = 165200
    min_volume = 0
    min_lat = 41.644670131999995
    max_lat = 42.022779861
    min_long = -87.933976504
    max_long = -87.52458738699998
    avg_temp_mean = 52.736361
    avg_temp_std = 20.625818
    avg_rain_mean = 0.117716
    avg_rain_std = 0.329548
    avg_snow_mean = 0.012092
    avg_snow_std = 0.104858
    length_mean = 439.04927
    length_std = 207.835484

    weather = weather[0]

    month = dt.month
    hour = dt.hour
    weekday = datetime.datetime.today().weekday()

    street_data['hour'] = hour
    street_data['month'] = month
    street_data['Avg Temp'] = weather[5]
    street_data['Snowfall'] = weather[4]
    street_data['Precipitation Water Equiv'] = weather[3]
    street_data['weekday'] = weekday

    street_data[['hour']] = (street_data[['hour']] - 12)/ 12
    street_data[['month']] = (street_data[['month']] - 6) / 6

    street_data = pd.concat([street_data,pd.get_dummies(street_data['weekday'], prefix='weekday')],axis=1)
    street_data = street_data.drop(['weekday'], axis=1)

    street_data[['Avg Temp']] = get_scaled_value(street_data[['Avg Temp']], avg_temp_mean, avg_temp_std)
    street_data[['Precipitation Water Equiv']] = get_scaled_value(street_data[['Precipitation Water Equiv']], avg_rain_mean, avg_rain_std)
    street_data[['Snowfall']] = get_scaled_value(street_data[['Snowfall']], avg_snow_mean, avg_snow_std)
    street_data[['length']] = get_scaled_value(street_data[['length']], avg_snow_mean, avg_snow_std)

    one_hot_cols = ['weekday_0',
        'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5',
        'weekday_6', 'class_1', 'class_2', 'class_3', 'class_4', 'class_5',
        'class_7', 'class_9', 'class_99', 'class_E', 'class_RIV', 'class_S']

    cols = set(street_data.columns.tolist())
    for col in one_hot_cols:
        if col not in cols:
            street_data[col] = 0

    X = street_data[['hour', 'latitude', 'length', 'longitude', 'month', 'volume',
        'Avg Temp', 'Precipitation Water Equiv', 'Snowfall', 'weekday_0',
        'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5',
        'weekday_6', 'class_1', 'class_2', 'class_3', 'class_4', 'class_5',
        'class_7', 'class_9', 'class_99', 'class_E', 'class_RIV', 'class_S',
        'one_way']]

    preds_y = clf.predict_proba(X)
    safety_scores = pd.Series(preds_y[:,0].tolist())
    street_segs = street_data[['latitude', 'longitude', 'street_nam']]
    street_segs['safety_score'] = safety_scores.values
    return street_segs

@app.route('/analyze-route', methods=['GET', 'POST'])
def analyze_route():
    data = request.json
    points =  data['points']
    subdivided_points = process_points(points)
    interpolated_points = fetch_interpolated_points(subdivided_points)
    roads = extract_roads(interpolated_points)
    route_weather = get_weather(interpolated_points)
    safety_df = get_model(street_data, route_weather)
    safety_score = make_safety_score(interpolated_points, safety_df, roads)
    
    response = {"snappedPoints": interpolated_points, "value":[safety_score]}
    return response

if __name__ == "__main__":
    app.run()