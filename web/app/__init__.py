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
import markdown
import re

# initiate Moment for datetime functions
moment = Moment()

app = Flask(__name__)

moment.init_app(app)

@app.route('/')
def index():
    # get month_limit from config file
    month_limit = os.environ.get('MONTH_LIMIT')
    # open JSON data
    json_data = open('./app/static/data/data.json')
    data = json.load(json_data)

    # get all the month labels
    month_labels = []
    for year in data['years']:
        if "months" in year:
            for month in year['months']:
                month_labels.append(month['month'] + " " + year['year'])
    month_labels = month_labels[-(int(month_limit)):]

    # get all the year labels
    year_labels = []
    for year in data['years']:
        if "months" in year:
            year_labels.append(year['year'])
    #
    # # get all the transportation modes
    # modes = []
    # for year in data['years']:
    #     if "months" in year:
    #         for month in year['months']:
    #             modes.append(month.keys())
    #             modes = list(modes)

    return render_template('index.html', month_limit=month_limit, data=data, month_labels=month_labels, year_labels=year_labels)

@app.route('/what')
def what():
    with open('README.md', 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
        html = re.sub("<h1.*?>\s", "", html)
    return render_template('what.html', html=html)
