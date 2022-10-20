# @name: data.py
# @creation_date: 2022-10-19
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Processes data
# @acknowledgements:

import random

def process_dataset(data, month_limit):
    # get all the month labels
    month_labels = []
    for year in data['years']:
        if "months" in year:
            for month in year['months']:
                month_labels.append(month['month'] + " " + year['year'])
    #show only the last x months of data (configured in environment file)
    month_labels = month_labels[-(int(month_limit)):]

    # get all the year labels
    year_labels = []
    for year in data['years']:
        if "months" in year:
            year_labels.append(year['year'])

    # get all the modes of transport
    modes = []
    for year in data['years']:
        if "months" in year:
            for month in year['months']:
                keys = month.keys()
                for key in keys:
                    modes.append(key)
    # remove duplicates
    modes = list(dict.fromkeys(modes))
    # remove month names data
    modes.remove('month')

    # for each mode, push data into an array and add to month_datasets
    month_datasets = []
    for mode in modes:
        mode_data = []
        for year in data['years']:
            if "months" in year:
                for month in year['months']:
                    if mode in month:
                        mode_data.append(month[mode])
                    else:
                        mode_data.append('0')
        #show only the last x months of data (configured in environment file)
        mode_data = mode_data[-(int(month_limit)):]
        random_colour = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        month_dataset = {"label": mode, "data": mode_data, "backgroundColor": random_colour}
        month_datasets.append(month_dataset)

    # for each mode, sum all the data for each year and add to year_datasets
    year_datasets = []
    for mode in modes:
        mode_data = []
        year_data = []
        for year in data['years']:
            if "months" in year:
                for month in year['months']:
                    if mode in month:
                        mode_data.append(month[mode])
                    # convert strings to floating-point numbers
                    mode_floats = [float(x) for x in mode_data]
                    # sum the list
                    mode_sum = sum(mode_floats)
                # add to the array of data for each year and reset mode_data
                year_data.append(mode_sum)
                mode_data = []
        random_colour = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        year_dataset = {"label": mode, "data": year_data, "backgroundColor": random_colour}
        year_datasets.append(year_dataset)

    return month_labels, year_labels, month_datasets, year_datasets
