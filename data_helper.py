"""This is a module to handle the csv data
Contains functions to help retrieve required data
"""

import pandas as pd

CONS_FILE_NAME = 'resources/resale_flat_prices.csv'


def get_dataframe():
    """Reads data from CSV using Pandas library

    Returns:
    dataframe: dataframe of all rows in the csv
    """
    return pd.read_csv(CONS_FILE_NAME)


def get_columnname():
    """Retrieves all columns from data table_frame
    """
    return get_dataframe().columns


def get_all_towns():
    """Retrieve all towns and sort them in ascending order

    Returns:
    list: list of all unique towns
    """
    return sorted(get_dataframe()['town'].unique())


def get_all_regions():
    """Retrieve all towns and sort them in ascending order

    Returns:
    list: list of all unique towns
    """
    return sorted(get_dataframe()['region'].unique())


def get_all_flat_types():
    """Retrieve all towns and sort them in ascending order

    Returns:
    list: list of all unique towns
    """
    return sorted(get_dataframe()['flat_type'].unique())


def get_filtered_towns(region):
    """Retrieve all towns based on region

    Returns:
    list: list of towns
    """
    df = get_dataframe()
    towns = df[df['region'] == region.upper()]['town'].unique()
    return sorted(towns)


def get_filtered_region(town):
    """Retrieve the region based on town

    Returns:
    list: list of filtered regions
    """
    df = get_dataframe()
    regions = df[df['town'] == town.upper()]['region'].unique()
    return sorted(regions)
