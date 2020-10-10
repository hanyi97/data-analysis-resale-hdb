"""This is a module to filter/search data in the summary table.
    The summary table will be changed based on what user has filtered/searched."""

import data_helper
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


# Find out your current working directory
import os
#print(os.getcwd())
# Display all of the files found in your current working directory
#print(os.listdir(os.getcwd()))

df = data_helper.get_dataframe()

print(df)