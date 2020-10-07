"""This is a module to plot bar graph
Based on average resale prices for different flat types.
Can be filtered by different town and year"""

import csv_helper
import numpy as np
from matplotlib import pyplot as plt


def add_flat_types():
    """Create a dictionary with all the flat types
    Assume that there are only these range of flat types

    Returns:
    dictionary: flat type as key and empty list as value
    """
    return {'1 ROOM': [], '2 ROOM': [], '3 ROOM': [], '4 ROOM': [], '5 ROOM': [], 'EXECUTIVE': [],
            'MULTI-GENERATION': []}


def filter_data(town, year):
    """Grouping all resale prices based on flat type
    Optional to filter by town

    Parameters:
    town (str): town can be empty if no filtering is selected
    year (str): year can be empty if no filtering is selected

    Returns:
    dictionary: flat type as key and list of resale prices based on flat type as value
    """
    data = add_flat_types()
    csv_data = csv_helper.get_dict_data()

    for line in csv_data:
        flat_type = line['flat_type']
        resale_price = float(line['resale_price'])

        # Filter by both town and year
        if town != '' and year != '':
            if line['town'].upper() == town and line['year'] == year:
                data[flat_type].append(resale_price)
        # Filter by town only
        elif town != '' and year == '':
            if line['town'].upper() == town:
                data[flat_type].append(resale_price)
        # Filter by year only
        elif town == '' and year != '':
            if line['year'] == year:
                data[flat_type].append(resale_price)
        # No filter
        else:
            data[flat_type].append(resale_price)
    return data


def get_data(town, year):
    """Calculate average for each flat type

    Parameters:
    town (str): town can be empty if no filtering is selected
    year (str): year can be empty if no filtering is selected

    Returns:
    dictionary: flat type as the key and average resale price as value
    """

    data = filter_data(town, year)
    for item in data:
        if len(data[item]) == 0:
            data[item].append(0)
        data[item] = round(sum(data[item]) / len(data[item]), 2)
    return data


def plot_bar_graph(town='', year=''):
    """Call this function to plot bar graph

    Parameters:
    town (str): town can be empty if no filtering is selected
    year (str): year can be empty if no filtering is selected
    """

    town = town.upper()
    data = get_data(town, year)
    town = 'SINGAPORE' if town == '' else town
    # Bar graph configurations
    ypos = np.arange(len(data))
    plt.barh(ypos, data.values())
    plt.yticks(ypos, data.keys())
    plt.ylabel('Average Resale Value (SGD)')
    plt.title('Town: (%s)\nAverage HDB resale value by flat type' % town)
    plt.show()
