# @name: __init__.py
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
import markdown
import re
import random
from . import data

# initiate Moment for datetime functions
moment = Moment()

app = Flask(__name__)

moment.init_app(app)

@app.route('/')
def index():
    # get month_limit from config file
    month_limit = os.environ.get('MONTH_LIMIT')

    # process personal transportation data
    # open JSON data
    json_data = open('./app/static/data/transport.json')
    transport_data = json.load(json_data)
    transport_processed = data.process_dataset(transport_data, month_limit)

    # process home energy data
    # open JSON data
    json_data = open('./app/static/data/energy.json')
    energy_data = json.load(json_data)
    energy_processed = data.process_dataset(energy_data, month_limit)

    return render_template('index.html', month_limit=month_limit, transport=transport_processed, energy=energy_processed)

@app.route('/what')
def what():
    with open('README.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
        html = re.sub("<h1.*?>\s", "", html)
        html = re.sub("<h2>about</h2>", "<h2>what is this?</h2>", html)
    return render_template('what.html', html=html)

@app.route('/transportation')
def transportation():
    # get month_limit from config file
    month_limit = os.environ.get('MONTH_LIMIT')

    # process personal transportation data
    # open JSON data
    json_data = open('./app/static/data/transport.json')
    transport_data = json.load(json_data)
    transport_processed = data.process_dataset(transport_data, month_limit)

    return render_template('transportation.html', month_limit=month_limit, transport=transport_processed)

@app.route('/energy')
def energy():
    # get month_limit from config file
    month_limit = os.environ.get('MONTH_LIMIT')

    # process home energy data
    # open JSON data
    json_data = open('./app/static/data/energy.json')
    energy_data = json.load(json_data)
    energy_processed = data.process_dataset(energy_data, month_limit)

    return render_template('energy.html', month_limit=month_limit, energy=energy_processed)
