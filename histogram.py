import matplotlib.pyplot as plt
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