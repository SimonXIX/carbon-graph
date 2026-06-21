# @name: england_functions.py
# @creation_date: 2026-02-02
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Retrieves and processes data from Google Sheets
# @acknowledgements:
# https://developers.google.com/sheets/api/quickstart/python
# https://stackoverflow.com/questions/74898227/can-i-using-google-sheet-api-only-with-api-key-or-using-client-id-and-client-sec
# https://stackoverflow.com/questions/74901976/how-to-give-permission-to-google-spreadsheet-created-by-service-account

# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from datetime import datetime

# VARIABLES

# a reasonable list of England-based keywords
england_keywords = [
    "coventry",
    "manchester",
    "sheffield",
    "warrington",
    "failsworth",
    "london",
    "newcastle",
    "crewe"
]

# SUBROUTINES

def process_england_data(data):

    # skip header
    rows = data[1:]

    # parse JSON data into (date, journey)
    parsed = [
        (datetime.strptime(d, "%Y-%m-%d").date(), j.lower())
        for d, j in rows
    ]

    # identify dates I was in England
    england_dates = set()

    for date, journey in parsed:
        if any(place in journey for place in england_keywords):
            england_dates.add(date)

    # sort England visit dates
    england_dates = sorted(england_dates)

    # compute gaps
    max_gap = 0
    max_gap_range = None

    for d1, d2 in zip(england_dates, england_dates[1:]):
        gap = (d2 - d1).days
        if gap > max_gap:
            max_gap = gap
            max_gap_range = (d1, d2)

    # calculate last trip to England
    last_england_date = max(england_dates)
    today = date.today()

    current_gap = (today - last_england_date).days

    return current_gap, last_england_date, max_gap, max_gap_range