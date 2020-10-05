import csv_helper
import numpy as np
from matplotlib import pyplot as plt


def add_flat_types():
    # # Assume that there are only these range of flat types
    # flat_types = ('1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENERATION')
    # data = {}
    #
    # # Add all the flat types in to dictionary
    # for flat_type in flat_types:
    #     data[flat_type] = []
    # return data

    # Assume that there are only these range of flat types
    return {'1 ROOM': [], '2 ROOM': [], '3 ROOM': [], '4 ROOM': [], '5 ROOM': [], 'EXECUTIVE': [],
            'MULTI-GENERATION': []}


def filter_data(region=''):
    data = add_flat_types()
    csv_data = csv_helper.get_dict_data()
    # Add all the values of each flat type
    if region != '':
        for line in csv_data:
            # Add items based on region
            if line['region'].upper() == region.upper():
                data[line['flat_type']].append(float(line['resale_price']))
    else:
        for line in csv_data:
            data[line['flat_type']].append(float(line['resale_price']))
    return data


# Calculate average for each flat type
def get_data(region):
    data = filter_data(region)
    for item in data:
        if len(data[item]) == 0:
            data[item].append(0)
        data[item] = round(sum(data[item]) / len(data[item]), 2)
    return data


# Call this function to plot bar graph
# Optional to filter results by region
# E.g. plot_bar_graph('EAST')
def plot_bar_graph(region=''):
    data = get_data(region)
    # Plot bar graph
    ypos = np.arange(len(data))
    plt.barh(ypos, data.values())
    plt.yticks(ypos, data.keys())
    plt.ylabel('Average Resale Value (SGD)')
    plt.title('Average HDB resale value by flat type')
    plt.show()
