# @name: __init__.py
# @version: 0.1
# @creation_date: 2022-06-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Initialises the app
# @acknowledgements:

from flask import Flask, render_template, request
from flask_moment import Moment
import requests
import urllib.request, json
import os

# initiate Moment for datetime functions
moment = Moment()

app = Flask(__name__)

moment.init_app(app)

@app.route('/')
def index():
    json_data = open('./app/static/data/data.json')
    data = json.load(json_data)
    return render_template('index.html', data=data)
