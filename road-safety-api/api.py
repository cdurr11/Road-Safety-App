from flask import Flask
from flask import request
import json
import flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    data = request.json
    print(data)
    response = flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run()