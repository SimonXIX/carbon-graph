# @name: sheets.py
# @creation_date: 2024-06-24
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Retrieves and processes data from Google Sheets
# @acknowledgements:
# https://developers.google.com/sheets/api/quickstart/python
# https://stackoverflow.com/questions/74898227/can-i-using-google-sheet-api-only-with-api-key-or-using-client-id-and-client-sec
# https://stackoverflow.com/questions/74901976/how-to-give-permission-to-google-spreadsheet-created-by-service-account

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os.path
import json
import random

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apiclient import discovery
from google.oauth2 import service_account

# VARIABLES

# If modifying these scopes, delete the file token.json.
scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# JSON file containing Google credentials
google_credentials = "/code/app/google_credentials.json"

# SUBROUTINES

# retrieve spreadsheet data from Google Sheets API
def get_data(spreadsheet_id, spreadsheet_range):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """

    credentials = service_account.Credentials.from_service_account_info(json.load(open(google_credentials)), scopes=scopes)

    try:
        service = build("sheets", "v4", credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=spreadsheet_id, range=spreadsheet_range)
            .execute()
        )
        values = result.get("values", [])

        #print(values)

        if not values:
            print("No data found.")
            return

        return values

    except HttpError as err:
        print(err)

# process month labels from data
def process_month_labels(data):
    # get all the month labels
    month_labels = []
    for row in data[1:]:
        if row[0] and 'Total' not in row[0]:
            month_labels.append(row[0][-3:] + " " + row[0][:4])
    return month_labels

# process year labels from data
def process_year_labels(data):
    # get all the year labels
    year_labels = []
    for row in data[1:]:
        if row[0] and 'Total' not in row[0]:
            if row[0][:4] not in year_labels:
                year_labels.append(row[0][:4])
    return year_labels

# process data into month_datasets
def process_month_datasets(data, modes, month_limit):
    # for each mode, push data into an array and add to month_datasets
    month_datasets = []
    for mode in modes:
        mode_data = []
        for month in data:
            if mode in month:
                mode_data.append(month[mode])
            else:
                mode_data.append('0')
        #show only the last x months of data (configured in environment file)
        mode_data = mode_data[-(int(month_limit)):]
        month_datasets.append({
            "label": mode, 
            "data": mode_data, 
            "backgroundColor": "#" + "%06x" % random.randint(0, 0xFFFFFF)
        })
    return month_datasets

# process data into year_datasets
def process_year_datasets(data, modes, years):
    # for each mode, sum all the data for each year and add to year_datasets
    year_datasets = []
    mode_sum = {}
    for mode in modes:
        mode_data = []
        year_data = []
        for year in years:
            for month in data:
                if year in month['month']:
                    if mode in month:
                        mode_data.append(month[mode])
                # convert strings to floating-point numbers
                mode_floats = [float(x) for x in mode_data]
                # sum the list
                mode_sum = sum(mode_floats)
            # add to the array of data for each year and reset mode_data
            year_data.append(mode_sum)
            mode_data = []
        year_datasets.append({
            "label": mode, 
            "data": year_data, 
            "backgroundColor": "#" + "%06x" % random.randint(0, 0xFFFFFF)
        })
    return year_datasets

# process transport pivot table data from Google Sheets spreadsheet
def process_transport_data(data, month_limit):
    month_labels = process_month_labels(data)
    #show only the last x months of data (configured in environment file)
    month_labels = month_labels[-(int(month_limit)):]

    year_labels = process_year_labels(data)
    
    # get all the modes of transport
    modes = []
    for row in data[1:]:
        if row[1] not in modes:
            modes.append(row[1])
    # remove duplicates
    modes = list(dict.fromkeys(modes))
    # remove empty strings
    modes = list(filter(None, modes))

    # format the data
    current_month = {}
    formatted_data = []
    for row in data[1:]:
        if row[0] and 'Total' not in row[0]:
            # new month starts
            if current_month:
                formatted_data.append(current_month)
            current_month = {"month": row[0]}
        if row[1] and 'Total' not in row[1]:
            # add transport data to current month
            current_month[row[1]] = row[6]
        if 'Total' in row[0]:
            # add last month
            if current_month:
                formatted_data.append(current_month)
            current_month = {}

    month_datasets = process_month_datasets(formatted_data, modes, month_limit)

    year_datasets = process_year_datasets(formatted_data, modes, year_labels)

    return month_labels, year_labels, month_datasets, year_datasets

# format transport pivot table data into form required for merging
def format_transport_data(data):
    output = {
        "years": []
    }

    current_year = None
    current_month = None

    for row in data[1:]:
        if row[0]:
            if "Total" in row[0]:
                current_month = None
                continue
            date_parts = row[0].split('-')
            year = date_parts[0]
            month = date_parts[1]

            if not current_year or current_year['year'] != year:
                current_year = {
                    "year": year,
                    "months": []
                }
                output["years"].append(current_year)
            
            current_month = {
                "month": month
            }
            current_year["months"].append(current_month)
        if current_month is not None:
            current_month[row[1]] = row[6]

    return output

# process energy pivot table data from Google Sheets spreadsheet
def process_energy_data(data, month_limit):
    month_labels = process_month_labels(data)
    #show only the last x months of data (configured in environment file)
    month_labels = month_labels[-(int(month_limit)):]

    year_labels = process_year_labels(data)

    # get all the modes of energy
    modes = ["electricity", "gas"]

    # format the data
    formatted_data = []
    for row in data[1:]:
        if row[0] and 'Total' not in row[0]:
            formatted_data.append({"month": row[0], "gas": row[3], "electricity": row[9]})

    month_datasets = process_month_datasets(formatted_data, modes, month_limit)

    year_datasets = process_year_datasets(formatted_data, modes, year_labels)

    return month_labels, year_labels, month_datasets, year_datasets

# format energy pivot table data into form required for merging
def format_energy_data(data):
    output = {
        "years": []
    }

    current_year = None
    current_month = None
    year_month_map = {}
        
    for row in data[1:]:
        if row[0]:
            date_parts = row[0].split('-')
            if len(date_parts) == 2:
                year = date_parts[0]
                month = date_parts[1]

                if year not in year_month_map:
                    year_month_map[year] = {}
                if month not in year_month_map[year]:
                    year_month_map[year][month] = {}

                year_month_map[year][month]['gas'] = row[3]

        if row[6]:
            date_parts = row[6].split('-')
            if len(date_parts) == 2:
                year = date_parts[0]
                month = date_parts[1]

                if year not in year_month_map:
                    year_month_map[year] = {}
                if month not in year_month_map[year]:
                    year_month_map[year][month] = {}

                year_month_map[year][month]['electricity'] = row[9]

    for year, months in year_month_map.items():
        year_data = {
            "year": year,
            "months": []
        }
        for month, values in months.items():
            month_data = {
                "month": month,
                "electricity": values.get('electricity', '0'),
                "gas": values.get('gas', '0')
            }
            year_data["months"].append(month_data)
        output["years"].append(year_data)

    return output

# format server table data
def format_server_data(data):

    server_data = []

    for row in data[1:]:
        kg = float(row[1])
        tonnes = kg / 1000
        server_data.append(tonnes)
        
    output = {
        "label": "cloud server hosting this site", 
        "data": server_data,
        "backgroundColor": "#" + "%06x" % random.randint(0, 0xFFFFFF)
    }

    return output