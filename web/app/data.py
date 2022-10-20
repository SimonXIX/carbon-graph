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

def merge_datasets(base_data, data_to_merge):

    base_data = sum_dataset(base_data[0], base_data[1])
    data_to_merge = sum_dataset(data_to_merge[0], data_to_merge[1])

    for year_index, year_base in enumerate(base_data['years']):
        if "months" in year_base:
            for month_index, month_base in enumerate(year_base['months']):
                year_value = year_base['year']
                month_value = month_base['month']
                for year_merge in data_to_merge['years']:
                    if year_merge['year'] == year_value:
                        for month_merge in year_merge['months']:
                            if month_merge['month'] == month_value:
                                month_base.update(month_merge)
                base_data['years'][year_index]['months'][month_index] = month_base

    return base_data

def sum_dataset(data, type):

    for year_index, year in enumerate(data['years']):
        if "months" in year:
            for month_index, month in enumerate(year['months']):
                month_value = month['month']
                month.pop('month')
                month_floats = [float(x) for x in month.values()]
                month_sum = sum(month_floats)
                month = {"month": month_value, type: month_sum}

                data['years'][year_index]['months'][month_index] = month

    return data

def add_annual_server_carbon(dataset, kg):

    kg = float(kg)
    tonnes = kg / 1000

    number_of_years = len(dataset[0]['data'])

    server_data = [tonnes] * number_of_years
    server_data[0] = '0'

    random_colour = "#" + "%06x" % random.randint(0, 0xFFFFFF)
    server_dataset = {"label": "cloud server hosting this site", "data": server_data, "backgroundColor": random_colour}
    dataset.append(server_dataset)

    return dataset
