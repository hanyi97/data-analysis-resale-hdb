import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import data_helper
from tabulate import tabulate

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()

# Display index, columns in df, number of entries, number of non-null values, column data type and memory information
print('\033[32;1m{}\033[0m'.format('The following are the information of the dataframe'))
df.info()

print('\n\033[32;1m{}\033[0m'.format('The following are the data analysis for resale price'))


def get_resale_price_year(year):
    """Get the table of description of the resale price for the specified year

    Parameters:
    year: 2017,2018,2019,"2017-2019"

    Returns:
    table: description of resale price - minimum resale price, maximum resale price,
    lower limit of the resale price, upper limit of the resale price, the first, second
    and third quartile of the resale price, interquartile range of resale price,
    mean of resale price, standard deviation of resale price,
    coefficient variation of resale price, skewness of resale price and numbers of outliers.
    """
    df = data_helper.get_dataframe()
    if year == 2017:
        df = df.loc[lambda df: df['year'] == 2017]
    elif year == 2018:
        df = df.loc[lambda df: df['year'] == 2018]
    elif year == 2019:
        df = df.loc[lambda df: df['year'] == 2019]
    else:
        df = df

    # the first, second, third quartile of resale price
    q1, q2, q3 = np.percentile(df['resale_price'], [25, 50, 75])
    # the interquartile range
    iqr = q3 - q1
    # the lower and upper limit of the box plot
    low_limit = q1 - (1.5 * iqr)
    up_limit = q3 + (1.5 * iqr)
    # the outliers
    rp_int_list = list(map(int, df['resale_price'].unique()))
    outlier_count = 0
    for x in rp_int_list:
        if not x <= up_limit:
            outlier_count += 1

    # description of resale price in table format
    resale_table = [['Min resale price:', df['resale_price'].min()],
                    ['lower limit:', low_limit],
                    ['Q1 resale price:', q1],
                    ['Q2 resale price:', q2],
                    ['Q3 resale price: ', q3],
                    ['upper limit:', up_limit],
                    ['Max resale price:', df['resale_price'].max()],
                    ['IQR resale price:', iqr],
                    ['MEAN resale price:', (df['resale_price'].mean())],
                    ['STD resale price:', (df['resale_price'].std())],
                    ['CV resale price:', (df['resale_price'].std() * 100 / df['resale_price'].mean())],
                    ['Skewness resale price:', (df['resale_price'].skew())],
                    ['Number of outliers:', outlier_count]]

    print(year, '\n', tabulate(resale_table, tablefmt='simple', numalign='right', floatfmt='.2f'), '\n')


get_resale_price_year('2017 - 2019')

# the histogram of resale price
sns.histplot(df['resale_price'], bins=50)
plt.title('Distribution of Resale Price in 2017-2019')
plt.show()

# the box and whiskers plot of resale price
df.boxplot(column='resale_price')
plt.title('Distribution of Resale Price in 2017-2019')
plt.show()

print('\033[32;1m{}\033[0m'.format('The following are the data analysis for year and resale price'))
# the distribution of 'town' - the mean, min, max for each town
year_result = df.groupby('year').agg({'resale_price': ['mean', 'min', 'max']}).apply(lambda x: round(x, 2))
print(year_result, '\n')

get_resale_price_year(2017), get_resale_price_year(2018), get_resale_price_year(2019)

# the box and whiskers plot of resale price for year 2017, 2018, 2019
sns.boxplot(
    x='year',
    y='resale_price',
    data=df
)
plt.title('Distribution of Resale Price in 2017, 2018, 2019')
plt.show()

print('\033[32;1m{}\033[0m'.format('The following are the data analysis for town'))
# the distribution of 'town' - the count for each town
print(df.groupby('town').size().astype(int).reset_index(name='count'), '\n')

# the bargraph of the count for each town from 2017-2019
df['town'].value_counts().plot.bar()
plt.title('Number of Resale Housing in Each Town in 2017-2019')
plt.show()

print('\033[32;1m{}\033[0m'.format('The following are the data analysis for town and resale price'))
# the distribution of 'town' - the mean, min, max for each town
town_result = df.groupby('town').agg({'resale_price': ['mean', 'min', 'max']}).apply(lambda x: round(x, 2))
print(town_result, '\n')

# the box and whiskers plot of resale price for each town from 2017-2019
ax = sns.boxplot(
    x='town',
    y='resale_price',
    data=df
)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha='right')
plt.title('Distribution of Resale Price for each town in 2017-2019')
plt.show()

print('\033[32;1m{}\033[0m'.format('The following are the data analysis for remaining lease and resale price'))


def get_remaining_lease_data(remaining_lease=''):
    """Group all remaining_lease of Resale Flats from Year 2017 - 2019

    Parameters:
    remaining_lease (str): remaining_lease can be empty if no filtering is needed

    Returns:
    dataframe: dataframe of filtered results
    """
    # read the dataset into a data table using Pandas
    df = data_helper.get_dataframe()
    # Validate remaining lease input
    if remaining_lease != '':
        df = df[(df['remaining_lease'] == remaining_lease)]
    return df.groupby('remaining_lease').size()


def plot_rlBargraph(remaining_lease=''):
    """Call this function to plot bar graph
    Able to save graph as png image

    Parameters:
    remaining_lease (str): remaining_lease can be empty if no filtering is needed
    """
    try:
        # Validate remaining lease input
        remaining_lease = str(remaining_lease) if remaining_lease != '' else remaining_lease
        # Retrieve remaining lease data
        df = get_remaining_lease_data(remaining_lease)

        # Plot Bar graph of Remaining Lease of Resale Flats from Year 2017 - 2019
        plt.bar(range(len(df)), df.values, align='center', color='m')
        plt.xticks(range(len(df)), df.index.values, size='small')
        # Set Set labels and title for bar graph
        plt.title('Remaining Lease of Resale Flats from Year 2017 - 2019')
        plt.xlabel('Remaining Lease (Years)')
        plt.ylabel('Count')
        plt.show()

    except IndexError:
        print('No data found!')

print(get_remaining_lease_data())
plot_rlBargraph()