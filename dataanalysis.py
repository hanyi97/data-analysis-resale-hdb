import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import data_helper

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()

# display the number of columns, number of entries, number of non-null values and data type
df.info()

# display distribution of 'year' - number of available resale housing in 2017,2018 and 2019
print(df.groupby('year').size())

# display the minimum and maximum value of the resale
print('Max resale price: ', df['resale_price'].max())
print('Min resale price: ', df['resale_price'].min())

# display the box and whisker plot
print(df.boxplot(column='resale_price'))
plt.show()

print('MEAN:', round(df['resale_price'].mean(), 2))
print('STD :', round(df['resale_price'].std(), 2))
print('CV  :', round(df['resale_price'].std() * 100 / df['resale_price'].mean(), 2))
print('Skewness :', round(df['resale_price'].skew(), 5))

# descriptive statistics summary
print(df['resale_price'].describe())


# incomplete - some are in my local
