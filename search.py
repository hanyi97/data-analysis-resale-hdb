"""This is a module to search data"""

import csv_helper
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# Find out your current working directory
import os
#print(os.getcwd())
# Display all of the files found in your current working directory
#print(os.listdir(os.getcwd()))

dataset = pd.read_csv("resources/resale_flat_prices.csv")

print(dataset)