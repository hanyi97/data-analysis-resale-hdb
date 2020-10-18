import tkinter as tk
from tkinter import ttk

from display_data import *
from search import *
from data_helper import *

from pandastable import Table
import bargraph
import matplotlib


matplotlib.use("TkAgg")

#Reusable font sizes
LARGE_FONT = ("Open Sans", 30)
NORM_FONT = ("Open Sans", 20)
SMALL_FONT = ("Open Sans", 15)


# Main Window
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


# Select Options Window
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


# # Top10 Data Window
# class Top10Window(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#         self.frames = {}
#         frame = View10Top(container, self)
#         self.frames[View10Top] = frame
#         frame.grid(row=0, column=0, sticky="nsew")
#         self.show_frame(View10Top)
#
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()


# Hanyi Function
class ViewCharts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Analyse Resale Flats by Region", font=NORM_FONT)
        label.pack(padx=10, pady=10)

        backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack(padx=10, pady=10)


# Kah En Function
class ViewSummary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Overview of Resale Flats Prices", font=NORM_FONT)
        label.pack(pady=10, padx=10)
        backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack()

        #get towns, regions,flatTypes data from csv
        df = data_helper.get_dataframe()
        towns = data_helper.get_all_towns()
        regions = data_helper.get_all_regions()
        flatTypes = data_helper.get_all_flatTypes()


        # Setting values for regions combo box
        listofRegions = sorted(regions)
        self.comboBoxRegion = ttk.Combobox(self, state="readonly")
        self.comboBoxRegion.pack(pady=0, padx=0)
        self.comboBoxRegion.bind('<<ComboboxSelected>>', lambda x: self.updateComboBox("region"))
        self.comboBoxRegion['values'] = listofRegions
        self.comboBoxRegion.current(0)

        # Setting values for town combo box
        listofTowns = sorted(towns)
        self.comboBoxTown = ttk.Combobox(self, state="readonly")
        self.comboBoxTown.pack(pady=0, padx=0)
        self.comboBoxTown.bind('<<ComboboxSelected>>', lambda x: self.updateComboBox(""))
        self.comboBoxTown['values'] = listofTowns
        self.comboBoxTown.current(0)

        # Setting values for flat types combo box
        listofFlatTypes = sorted(flatTypes)
        self.comboxBoxFlatTypes = ttk.Combobox(self, state="readonly")
        self.comboxBoxFlatTypes.pack(pady=0, padx=0)
        self.comboxBoxFlatTypes['values'] = listofFlatTypes
        self.comboxBoxFlatTypes.set("Select Flat Type")

        filterButton = tk.Button(self, text="Filter", command=self.updateTable)
        filterButton.pack()


        #Creating table for summary
        frame = Frame(self)
        frame.pack()
        self.table = Table(frame, dataframe=df,
                      height=400, width=1100)
        self.table.show()

        top10button = tk.Button(self, text="View Top 10", font=SMALL_FONT,
                                command=lambda: self.displayTop10())
        top10button.pack(padx=10, pady=10)

    #resets town dropdown based on region
    def updateComboBox(self,control):
        if control == "region":
            listofTowns = get_town_acrd_region(self.comboBoxRegion.get())
            self.comboBoxTown['values'] = listofTowns
            self.comboBoxTown.current(0)

    def updateTable(self):
        #repopulate dictionary for table based on new selected drop down value
        filters = {"town": self.comboBoxTown.get(), "flat_type": self.comboxBoxFlatTypes.get()}
        print("filters",filters)
        valuesBasedOnFilters = get_filtered_data(filters)
        print("values", valuesBasedOnFilters)


        # #clears existing summmary table
        # self.table.clearTable()


        #replot table with updated data
        #not complete
        frame = Frame(self)
        frame.pack()
        table = Table(frame, dataframe=valuesBasedOnFilters
                           , height=400, width=1100)
        table.update()

    # def displayTop10(self):
    #     mainApp = Top10Window()
    #     mainApp.title("Top 10 Resale Flats")
    #     mainApp.geometry("800x800")
    #     mainApp.mainloop()



# # Kah En Function
# class View10Top(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Top 10 Resale Flats Prices", font=NORM_FONT)
#         label.pack(pady=10, padx=10)
#

app = WelcomeWindow()
app.title("HDB Resale Flats Analyser")
app.geometry("900x700")
app.mainloop()
