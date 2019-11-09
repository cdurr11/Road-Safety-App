import requests
from flask import Flask
from flask import request
import json
import flask
from flask_cors import CORS
from API_KEY import api_key


app = Flask(__name__)
CORS(app)


def generate_path_request(points):
    path_string = ""
    for point_i in range(len(points)):
        path_string = path_string + str(points[point_i][0]) + "," + str(points[point_i][1])
        if point_i != len(points) - 1:
            path_string += "|"
    
    return path_string
        

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    data = request.json
    response = flask.jsonify({'some': 'data'})
    points =  data['points']
    path_string = generate_path_request(points)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response_roads = requests.get('https://roads.googleapis.com/v1/snapToRoads?path='+path_string+'&interpolate=true&key='+api_key).content
    return response_roads

if __name__ == "__main__":
    app.run()