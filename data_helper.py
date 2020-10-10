"""This is a module to handle the csv data
It includes three functions
One function to retrieve data as a dataframe
One function to retrieve data as a list
One function to retrieve data as dictionary
"""

import csv
import pandas as pd
CONST_filename = 'resources/resale_flat_prices.csv'


def get_dataframe():
    """Reads data from CSV using Pandas library

    Returns:
    dataframe: dataframe of all rows in the csv
    """
    return pd.read_csv(CONST_filename)


def get_all_towns():
    """Retrieve all towns and sort them in ascending order

    Returns:
    list: list of all unique towns
    """
    return sorted(get_dataframe()['town'].unique())


def get_data():
    """Reads data from CSV and returns a list of each row
    Note: first item in list are the columns of the dataset
    Returns:
    list: list of all rows in csv file including header row
    """
    with open(CONST_filename, 'r', encoding='utf-8-sig') as csv_file:
        return list(csv.reader(csv_file, delimiter=','))


def get_dict_data():
    """Reads data from CSV and returns it as a list of dictionaries of each row
    {'header': 'value'}
    Returns:
    list: list of dictionaries of each row of data
    """
    with open(CONST_filename, 'r', encoding='utf-8-sig') as csv_file:
        return list(csv.DictReader(csv_file, delimiter=','))