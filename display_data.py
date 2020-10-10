"""This is a module to display dataset as a summary table
    For user to view everything in the dataset"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import data_helper

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()

# Check data types
print(df.dtypes)


# Function to display dataset.
def display_dataset():
    return print(df)


# Display no. of rows and columns in dataset
print('This dataset has %d rows and %d columns.' % (df.shape[0], df.shape[1]))
# Call function to display dataset
display_dataset()
