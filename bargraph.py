"""This is a module to plot bar graph
Based on average resale prices for different flat types.
Can be filtered by different region"""

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


def filter_data(region):
    """Grouping all resale prices based on flat type
    Optional to filter by region

    Parameters:
    region (str): region can be empty if no filtering is selected

    Returns:
    dictionary: flat type as key and list of resale prices based on flat type as value
    """
    data = add_flat_types()
    csv_data = csv_helper.get_dict_data()
    # Add all the values of each flat type
    if region != '':
        for line in csv_data:
            # Add items based on region
            if line['region'].upper() == region:
                data[line['flat_type']].append(float(line['resale_price']))
    else:
        for line in csv_data:
            data[line['flat_type']].append(float(line['resale_price']))
    return data


def get_data(region):
    """Calculate average for each flat type

    Parameters:
    region (str): region can be empty if no filtering is selected

    Returns:
    dictionary: flat type as the key and average resale price as value
    """
    data = filter_data(region)
    for item in data:
        if len(data[item]) == 0:
            data[item].append(0)
        data[item] = round(sum(data[item]) / len(data[item]), 2)
    return data


def plot_bar_graph(region=''):
    """Call this function to plot bar graph

    Parameters:
    region (str): region can be empty if no filtering is selected
    """

    region = region.upper()
    data = get_data(region)
    region = 'SINGAPORE' if region == '' else region

    # Bar graph configurations
    ypos = np.arange(len(data))
    plt.barh(ypos, data.values())
    plt.yticks(ypos, data.keys())
    plt.ylabel('Average Resale Value (SGD)')
    plt.title('Region: (%s)\nAverage HDB resale value by flat type' % region)
    plt.show()
