import csv_helper
import numpy as np
from matplotlib import pyplot as plt


def add_flat_types():
    # Assume that there are only these range of flat types
    flat_types = ('1 ROOM', '2 ROOM', '3 ROOM', '4 ROOM', '5 ROOM', 'EXECUTIVE', 'MULTI-GENERATION')
    data = {}

    # Add all the flat types in to dictionary
    for flat_type in flat_types:
        data[flat_type] = []
    return data


def add_values():
    data = add_flat_types()
    # Add all the values of each flat type
    for line in csv_helper.get_dict_data():
        resale_price = float(line['resale_price'])
        data[line['flat_type']].append(resale_price)
    return data


def get_data():
    data = add_values()
    # Calculate average for each flat type
    for item in data:
        data[item] = round(sum(data[item]) / len(data[item]), 2)
    return data


def plot_bar_graph():
    data = get_data()
    # Plot bar graph
    ypos = np.arange(len(data))
    plt.barh(ypos, data.values())
    plt.yticks(ypos, data.keys())
    plt.ylabel('Average Resale Value (SGD)')
    plt.title('Average HDB resale value by flat type')
    plt.show()
