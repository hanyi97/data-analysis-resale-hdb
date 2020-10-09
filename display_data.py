import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv_helper

# read the dataset into a data table using Pandas
df = csv_helper.get_dataframe()


# Check data types
print(df.dtypes)

# display dataset function
def display_dataset():
    return print(df)


# display no. of rows and columns in dataset
print('This dataset has %d rows and %d columns.' % (df.shape[0], df.shape[1]))
# display dataset
display_dataset()
