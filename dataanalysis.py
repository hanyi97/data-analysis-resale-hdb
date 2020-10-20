import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import data_helper
from tabulate import tabulate
import search

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()

# Display index, columns in df, number of entries, number of non-null values, column data type and memory information
print("\033[32;1m{}\033[0m".format("The following are the information of the dataframe"))
df.info()

print("\n\033[32;1m{}\033[0m".format("The following are the data analysis for resale price"))


def resale_price_year(year):
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
    rp_int_list = list(map(int, search.get_unique("resale_price")))
    outlier_count = 0
    for x in rp_int_list:
        if not x <= up_limit:
            outlier_count += 1

    # description of resale price in table format
    resale_table = [["Min resale price:", df['resale_price'].min()], ['lower limit:', low_limit],
                    ['Q1 resale price:', q1],
                    ['Q2 resale price:', q2], ['Q3 resale price: ', q3],
                    ["Max resale price:", df['resale_price'].max()], ['IQR resale price:', iqr],
                    ['upper limit:', up_limit],
                    ['MEAN resale price:', (df['resale_price'].mean())],
                    ['STD resale price:', (df['resale_price'].std())],
                    ['CV resale price:', (df['resale_price'].std() * 100 / df['resale_price'].mean())],
                    ['Skewness resale price:', (df['resale_price'].skew())],
                    ['Number of outliers:', outlier_count]]

    print(year, "\n", tabulate(resale_table, tablefmt="simple", numalign="right", floatfmt=".2f"), "\n")


resale_price_year("2017 - 2019")

# the histogram of resale price
sns.histplot(df['resale_price'], bins=50)
plt.title("Distribution of Resale price in 2017-2019")
plt.show()

# the box and whiskers plot of resale price
df.boxplot(column='resale_price')
plt.title("Distribution of Resale price in 2017-2019")
plt.show()

print("\033[32;1m{}\033[0m".format("The following are the data analysis for year and resale price"))
# the distribution of 'town' - the mean, min, max for each town
year_result = df.groupby('year').agg({'resale_price': ['mean', 'min', 'max']}).apply(lambda x: round(x, 2))
print(year_result, "\n")

resale_price_year(2017), resale_price_year(2018), resale_price_year(2019)

# the box and whiskers plot of resale price for year 2017, 2018, 2019
sns.boxplot(
    x='year',
    y='resale_price',
    data=df
)
plt.title("Distribution of Resale price in 2017, 2018, 2019")
plt.show()

print("\033[32;1m{}\033[0m".format("The following are the data analysis for town"))
# the distribution of 'town' - the count for each town
print(df.groupby('town').size().astype(int).reset_index(name='count'), "\n")

# the bargraph of the count for each town from 2017-2019
df['town'].value_counts().plot.bar()
plt.title("Number of Resale Housing in Each Town in 2017-2019")
plt.show()

print("\033[32;1m{}\033[0m".format("The following are the data analysis for town and resale price"))
# the distribution of 'town' - the mean, min, max for each town
town_result = df.groupby('town').agg({'resale_price': ['mean', 'min', 'max']}).apply(lambda x: round(x, 2))
print(town_result, "\n")

# the box and whiskers plot of resale price for each town from 2017-2019
ax = sns.boxplot(
    x='town',
    y='resale_price',
    data=df
)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.title("Distribution of Resale Price for each town in 2017-2019")
plt.show()
