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
        year = int(year) if year != '' else year
        df = get_filtered_data(town, year)
        town = 'SINGAPORE' if town == '' else town

        # GUI configurations
        window = tk.Tk()
        window.title('Bar graph based on average resale price by flat type')
        window.geometry("1920x480")

        # Creating a figure
        fig = Figure(figsize=(20, 5))

        # adding the subplot
        ax = fig.add_subplot(111)

        # Bar graph configuration
        bargraph = df.plot.barh(color='navy', ax=ax)
        bargraph.set_xlabel('Average Resale Value (SGD)')
        bargraph.set_ylabel('HDB Flat Type')
        bargraph.set_title('Town: (%s)\nAverage HDB resale value by flat type' % town)
        if export:
            bargraph.get_figure().savefig('resources/bargraph.png', bbox_inches='tight')

        # Creating the Tkinter canvas containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()

        # Placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()

        # Run the gui
        window.mainloop()
    except ValueError:
        print("Year is not an integer!")
    except IndexError:
        print("No data found!")
