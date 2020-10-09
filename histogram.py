import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import data_helper


def get_remaining_lease_data(remaining_lease=""):
    """Group all remaining_lease of Resale Flats from Year 2017 - 2019

    Parameters:
    remaining_lease (str)

    Returns:
    dataframe: dataframe of filtered results
    """
    # read the dataset into a data table using Pandas
    df = data_helper.get_dataframe()
    if remaining_lease != "":
        df = df[(df['remaining_lease'] == remaining_lease)]
    return df.groupby('remaining_lease').size()


def plot_rlBargraph(remaining_lease=''):
    """Call this function to plot bar graph
    Able to save graph as png image

    Parameters:
    remaining_lease (str): remaining_lease can be empty if no filtering is needed
    """
    try:
        # Retrieve data
        remaining_lease = str(remaining_lease) if remaining_lease != '' else remaining_lease
        df = get_remaining_lease_data(remaining_lease)

        # Plot Histogram of Remaining Lease of Resale Flats from Year 2017 - 2019
        plt.bar(range(len(df)), df.values, align='center', color='m')
        plt.xticks(range(len(df)), df.index.values, size='small')
        plt.title("Remaining Lease of Resale Flats from Year 2017 - 2019")
        plt.xlabel('Remaining Lease (Years)')
        plt.ylabel('Count')
        plt.show()

    except IndexError:
        print("No data found!")

def get_FAS_data(floor_area_sqm='', resale_price=''):
    """Group all resale prices based on floor_area_sqm
    Optional to filter by town or year (or both)

    Parameters:
    floor_area_sqm (str): filter data by floor_area_sqm (optional)
    resale_price (str): filter data by resale_price (optional)

    Returns:
    dataframe: dataframe of filtered results
    """
    df = data_helper.get_dataframe()
    if floor_area_sqm != '' and resale_price != '':
        df = df[(df['floor_area_sqm'] == floor_area_sqm) & (df['resale_price'] == resale_price)]
    elif floor_area_sqm != '':
        df = df[df['floor_area_sqm'] == floor_area_sqm]
    elif resale_price != '':
        df = df[df['resale_price'] == resale_price]
    return df.groupby('floor_area_sqm')['resale_price'].mean().round(2)



# Bargraph is very WRONG, need to rethink and redo!!!
def plot_FAS_RSP_Bargraph(floor_area_sqm='', resale_price='', export=False):
    """Call this function to plot bar graph
    Able to save graph as png image

    Parameters:
    town (str): town can be empty if no filtering is needed
    year (str): year can be empty if no filtering is needed
    export (bool): pass in True to save graph as pdf
    """
    try:
        floor_area_sqm = float(floor_area_sqm) if floor_area_sqm != '' else floor_area_sqm
        resale_price = int(resale_price) if resale_price != '' else resale_price
        df = get_FAS_data(floor_area_sqm, resale_price)

        # Plot Histogram of Remaining Lease of Resale Flats from Year 2017 - 2019
        plt.bar(range(len(df)), df.values, align='center', color='b')
        plt.xticks(range(len(df)), df.index.values, size='small')
        plt.title('Average HDB resale value by Floor area sqm')
        plt.xlabel('Floor area sqm')
        plt.ylabel('Average Resale Value (SGD)')
        plt.show()

    except:
        print("No data found!")
