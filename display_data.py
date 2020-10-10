"""This is a module to display dataset as a summary table
    For user to view everything in the dataset"""

import pandas as pd
import data_helper
from tkinter import *
from pandastable import Table, TableModel

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()

# Function to display dataset.
def display_dataset():
    return print(df)

# Display no. of rows and columns in dataset
print('This dataset has %d rows and %d columns.' % (df.shape[0], df.shape[1]))
# Call function to display dataset
display_dataset()
