"""This is a module to plot bar graph
Based on average resale prices for different flat types.
Can be filtered by town and year
Can export graph as png image"""

import data_helper
from matplotlib import pyplot as plt


def get_filtered_data(town='', year=''):
    """Group all resale prices based on flat type
    Optional to filter by town or year (or both)

    Parameters:
    town (str): filter data by town (optional)
    year (str): filter data by year (optional)

    Returns:
    dataframe: dataframe of filtered results
    """
    df = data_helper.get_dataframe()
    if town != '' and year != '':
        df = df[(df['town'] == town) & (df['year'] == year)]
    elif town != '':
        df = df[df['town'] == town]
    elif year != '':
        df = df[df['year'] == year]
    return df.groupby('flat_type')['resale_price'].mean().round(2)


def plot_bar_graph(town='', year='', export=False):
    """Call this function to plot bar graph
    Able to save graph as png image

    Parameters:
    town (str): town can be empty if no filtering is needed
    year (str): year can be empty if no filtering is needed
    export (bool): pass in True to save graph as pdf
    """
    try:
        town = town.upper()
        df = get_filtered_data(town, int(year))
        town = 'SINGAPORE' if town == '' else town
        # Bar graph configurations
        plt.clf()
        bargraph = df.plot.barh(color='navy', figsize=(20, 5))
        bargraph.set_xlabel('Average Resale Value (SGD)')
        bargraph.set_ylabel('Flat Type')
        bargraph.set_title('Town: (%s)\nAverage HDB resale value by flat type' % town)
        if export:
            plt.savefig('resources/bargraph.png', bbox_inches='tight')
        plt.show()
    except ValueError:
        print("Year is not an integer!")
    except IndexError:
        print("No data found!")
