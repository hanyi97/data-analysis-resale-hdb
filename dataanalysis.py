import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv_helper

# read the dataset into a data table using Pandas
df = csv_helper.get_dataframe()

# display all the data
#df.show()

# the data type, number of columns, number of entries, number of non-null values
df.info()

# distribution of 'region' - number of available resale housing in 2017,2018 and 2019
print(df.groupby('region').size())

print('Max resale price: ', df['resale_price'].max())
print('Min resale price: ', df['resale_price'].min())

# first visualise the box and whisker plot
print(df.boxplot(column='resale_price'))
plt.show()

# further discover statistics on variable 'resale_price'
# A low standard deviation (std) means that the data points tend to
# be close to the mean.
# A high std indicates that the data points are scattered.
# coefficient of variation(CV) to visualise the dispersion.
# skewness level to know the distribution level: positively skewed/ normally distributed/ negatively skewed.
print('MEAN:', round(df['resale_price'].mean(), 2))
print('STD :', round(df['resale_price'].std(), 2))
print('CV  :', round(df['resale_price'].std() * 100 / df['resale_price'].mean(), 2))
print('Skewness :', round(df['resale_price'].skew(), 5))

#descriptive statistics summary
print(df['resale_price'].describe())



# incomplete - some are in my local
