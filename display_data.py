import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv_helper

# read the dataset into a data table using Pandas
df = pd.read_csv("resources/resale_flat_prices.csv")
df.show()
# #descriptive statistics summary
# print(df['resale_price'].describe())
#
# print(df.boxplot(column='resale_price'))
# plt.show()