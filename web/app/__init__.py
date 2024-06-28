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
from . import sheets

# initiate Moment for datetime functions
moment = Moment()

app = Flask(__name__)

moment.init_app(app)

@app.route('/')
def index():
    # get the ID and range of the pivot tables from config file
    spreadsheet_id = os.environ.get('SPREADSHEET_ID')
    transport_range = os.environ.get('TRANSPORT_PIVOT_TABLE_RANGE')
    energy_range = os.environ.get('ENERGY_PIVOT_TABLE_RANGE')
    # get data_source from config file
    data_source = os.environ.get('DATA_SOURCE')
    # get month_limit from config file
    month_limit = os.environ.get('MONTH_LIMIT')
    # get cloud server carbon usage from config file
    server_carbon = os.environ.get('SERVER_CARBON')

    if data_source == 'manual':
        # open personal transportation data
        json_data = open('./app/static/data/transport.json')
        transport_data = []
        transport_data.append(json.load(json_data))
        transport_data.append('personal transportation')

        # open home energy data
        json_data = open('./app/static/data/energy.json')
        energy_data = []
        energy_data.append(json.load(json_data))
        energy_data.append('home energy')

        merged_data = data.merge_datasets(transport_data, energy_data)

        merged_processed = data.process_dataset(merged_data, month_limit)

        merged_processed = list(merged_processed)
        merged_processed[3] = data.add_annual_server_carbon(merged_processed[3], server_carbon)

        return render_template('index.html', month_limit=month_limit, total=merged_processed)

    elif data_source == 'sheets':
        # get and format personal transportation data
        transport_data = []
        raw_data = sheets.get_data(spreadsheet_id, transport_range)
        transport_data.append(sheets.format_transport_data(raw_data))
        transport_data.append('personal transportation')

        # get and format home energy data
        energy_data = []
        raw_data = sheets.get_data(spreadsheet_id, energy_range)
        energy_data.append(sheets.format_energy_data(raw_data))
        energy_data.append('home energy')

        merged_data = data.merge_datasets(transport_data, energy_data)

        merged_processed = data.process_dataset(merged_data, month_limit)

        merged_processed = list(merged_processed)
        merged_processed[3] = data.add_annual_server_carbon(merged_processed[3], server_carbon)

        return render_template('index.html', month_limit=month_limit, total=merged_processed)

    else: 
        raise ValueError("Invalid data source")

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
    # get the ID and range of the transport pivot table from config file
    spreadsheet_id = os.environ.get('SPREADSHEET_ID')
    spreadsheet_range = os.environ.get('TRANSPORT_PIVOT_TABLE_RANGE')
    # get data_source from config file
    data_source = os.environ.get('DATA_SOURCE')
    # get month_limit from config file
    month_limit = os.environ.get('MONTH_LIMIT')

    if data_source == 'manual':
        # process personal transportation data
        # open JSON data
        json_data = open('./app/static/data/transport.json')
        transport_data = json.load(json_data)
        transport_processed = data.process_dataset(transport_data, month_limit)

        return render_template('transportation.html', month_limit=month_limit, transport=transport_processed)
    
    elif data_source == 'sheets':
        transport_data = sheets.get_data(spreadsheet_id, spreadsheet_range)
        transport_processed = sheets.process_transport_data(transport_data, month_limit)

        return render_template('transportation.html', month_limit=month_limit, transport=transport_processed)

    else: 
        raise ValueError("Invalid data source")

@app.route('/energy')
def energy():
    # get the ID and range of the transport pivot table from config file
    spreadsheet_id = os.environ.get('SPREADSHEET_ID')
    spreadsheet_range = os.environ.get('ENERGY_PIVOT_TABLE_RANGE')
    # get data_source from config file
    data_source = os.environ.get('DATA_SOURCE')
    # get month_limit from config file
    month_limit = os.environ.get('MONTH_LIMIT')

    if data_source == 'manual':
        # process home energy data
        # open JSON data
        json_data = open('./app/static/data/energy.json')
        energy_data = json.load(json_data)
        energy_processed = data.process_dataset(energy_data, month_limit)

        return render_template('energy.html', month_limit=month_limit, energy=energy_processed)
    
    elif data_source == 'sheets':
        energy_data = sheets.get_data(spreadsheet_id, spreadsheet_range)
        energy_processed = sheets.process_energy_data(energy_data, month_limit)

        return render_template('energy.html', month_limit=month_limit, energy=energy_processed)

    else: 
        raise ValueError("Invalid data source")