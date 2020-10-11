import tkinter as tk
from tkinter import ttk

from display_data import *
from search import *

import pandas as pd
from pandastable import Table

LARGE_FONT = ("Open Sans", 30)
NORM_FONT = ("Open Sans", 20)
SMALL_FONT = ("Open Sans", 15)

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()


class WelcomeWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (SelectOptions, ViewCharts, ViewSummary):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(SelectOptions)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class SelectOptions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.createLabels()
        self.createButtons(controller)

    def createLabels(self):
        header = tk.Label(self, text="HDB Resale Flats Analyser", font=LARGE_FONT)
        label = tk.Label(self,
                         text="This service enables you to check the resale flat prices within the last 3 years based on regions, "
                              "towns and flat-types.",
                         font=SMALL_FONT, wraplength=450)
        header.pack(padx=0, pady=20)
        label.pack(padx=10, pady=10)

    def createButtons(self, controller):
        chartsBTN = tk.Button(self, text="View Charts", height=5, width=30, font=SMALL_FONT,
                              command=lambda: controller.show_frame(ViewCharts))
        chartsBTN.pack(pady=10, padx=10)
        summaryBTN = tk.Button(self, text="View Summary", height=5, width=30, font=SMALL_FONT,
                               command=lambda: controller.show_frame(ViewSummary))
        summaryBTN.pack()

    # def displaySummary(self):
    #
    #     mainApp = ViewSummaryWindow()
    #     mainApp.title("Overview of Resale Flat Prices")
    #     mainApp.geometry("900x900")
    #     mainApp.mainloop()


class ViewCharts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Analyse Resale Flats by Region", font=NORM_FONT)
        label.pack(padx=10, pady=10)

        backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack(padx=10, pady=10)


# class ViewSummaryWindow(tk.Tk):
#
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#         self.frames = {}
#         frame = ViewSummary(container, self)
#         self.frames[ViewSummary] = frame
#         frame.grid(row=0, column=0, sticky="nsew")
#         self.show_frame(ViewSummary)
#
#
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()


class ViewSummary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Overview of Resale Flats Prices", font=NORM_FONT)
        label.pack(pady=10, padx=10)

        backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack()

        # List of filters from the csv file
        # listofFilters = sorted(get_filtered_data(in_col))
        #
        # for x in listofFilters:
        #      # combobox
        #     self.comboBoxOrderGroup = ttk.Combobox(self, state="readonly")
        #     self.comboBoxOrderGroup.pack(pady=0, padx=0)
        #     # self.comboBoxOrderGroup.bind('<<ComboboxSelected>>',
        #     #                              lambda x: self.updateGraphNic(self.comboBoxOrderGroup.get()))
        #     columnvalues = df.values.ravel()
        #     print(columnvalues)
        #     unqiue= pd.unique(listofFilters)
        #     print(unqiue)
        #
        #     self.comboBoxOrderGroup['values'] = listofFilters
        #     self.comboBoxOrderGroup.current(0)

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        df = data_helper.get_dataframe()


        frame = Frame(self)
        frame.pack()
        table = Table(frame, dataframe=df)
        table.show()



app = WelcomeWindow()
app.title("HDB Resale Flats Analyser")
app.geometry("600x600")
app.mainloop()
