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

class Top10ViewWindow(Frame):
    """Basic test frame for the table"""
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('HDB Resale Flats Analyser')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        df = data_helper.get_dataframe()
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return

app = Top10ViewWindow()
#launch the app
app.mainloop()