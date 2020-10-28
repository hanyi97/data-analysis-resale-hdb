"""This is a module to plot bar graph
Based on average resale prices for different flat types.
Can be filtered by town"""


from numpy import arange
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from data_helper import get_dataframe


def get_filtered_data(town=''):
    """Group all average resale prices based on flat type
    Optional to filter by town if being passed as parameter

    Parameters:
    town (str): filter data by town (optional)

    Returns:
    dataframe: dataframe of filtered results
    """
    df = get_dataframe()
    if town != '':
        df = df[df['town'] == town]
    return df.groupby('flat_type')['resale_price'].mean().round(2)


def plot_bargraph(town=''):
    """Call this function to plot bar graph
    The updated graph will be auto saved whenever this function is called

    Parameters:
    town (str): town can be empty if no filtering is needed
    export (bool): pass in True to save graph as pdf

    Returns:
    figure: figure of the bar graph
    """
    try:
        if town == 'SELECT TOWN':
            town = ''
        town = town.upper()
        df = get_filtered_data(town)
        if len(df) == 0:
            raise IndexError('No data found!')
        # Set town to Singapore when no town is selected
        town = 'SINGAPORE' if town == '' else town

        # Create a figure
        fig = Figure(figsize=(20, 5))
        ax = fig.add_subplot(111)
        # Bar graph configuration

        bargraph = df.plot.barh(color='#E7B75F', ax=ax, zorder=2, label='Average Resale Pricing')
        # Set x ticks to frequency of 100,000
        start, end = bargraph.get_xlim()
        bargraph.xaxis.set_ticks(arange(start, end, 100000))
        # Add comma to resale flat prices
        bargraph.get_xaxis().set_major_formatter(FuncFormatter(lambda x, loc: '{:,}'.format(int(x))))
        # Remove borders
        bargraph.spines['right'].set_visible(False)
        bargraph.spines['top'].set_visible(False)
        bargraph.spines['left'].set_visible(False)
        bargraph.spines['bottom'].set_visible(False)
        # Draw vertical axis lines
        ticks = ax.get_xticks()
        for tick in ticks:
            bargraph.axvline(x=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
        # Set average resale value to bar labels
        for i in bargraph.patches:
            price = i.get_width()
            bargraph.text(price + .3, i.get_y() + .15, str('${:,}'.format(int(price))),
                          fontsize=10,
                          color='dimgrey')
        # Style labels and title
        label_style = {'fontsize': 9, 'fontweight': 'heavy'}
        bargraph.set_xlabel('Average Resale Value (SGD)',
                            fontdict=label_style)
        bargraph.set_ylabel('HDB Flat Type',
                            fontdict=label_style)
        bargraph.set_title('Town: (%s)\nAverage HDB resale value by flat type' % town,
                           fontdict={'fontsize': 10, 'fontweight': 'heavy'})
        bargraph.legend(loc='lower right', bbox_to_anchor=(1., 1.02), borderaxespad=0.)

        return fig
    except ValueError:
        print('Cannot convert data to an integer!')
    except IndexError as e:
        print(e)
