import tkinter as tk
from tkinter import ttk
from search import *
import data_helper as dh
from pandastable import Table, TableModel
import bargraph
import matplotlib

matplotlib.use("TkAgg")

# Reusable font sizes
LARGE_FONT = ("Open Sans", 30)
NORM_FONT = ("Open Sans", 16)
SMALL_FONT = ("Open Sans", 15)
VALIDAITON_FONT = ("Open Sans", 12)


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
                         text="This service enables you to check the resale flat prices within the last 3 years based "
                              "on regions, "
                              "towns and flat-types.",
                         font=NORM_FONT, wraplength=450)
        header.pack(padx=0, pady=20)
        label.pack(padx=10, pady=10)

    def createButtons(self, controller):
        chartsBTN = tk.Button(self, text="View Charts", height=5, width=30, font=NORM_FONT,
                              command=lambda: controller.show_frame(ViewCharts))
        chartsBTN.pack(pady=10, padx=10)
        summaryBTN = tk.Button(self, text="View Summary", height=5, width=30, font=NORM_FONT
                               ,
                               command=lambda: controller.show_frame(ViewSummary))
        summaryBTN.pack()


# Export Data Window
class ExportResults(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Export your results", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # container = tk.Frame(self)
        # container.pack(side="top", fill="both", expand=True)
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)
        # self.frames = {}

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Hanyi, Faiz Function
class ViewCharts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Analyse Resale Flats by Region", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        backbutton = tk.Button(self, text="Back to Home", font=SMALL_FONT,
                               command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack(padx=10, pady=10)



# Joey Function
class ViewSummary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Overview of Resale Flats Prices", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        backbutton = tk.Button(self, text="Back to Home", font=SMALL_FONT,
                               command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack(padx=5, pady=5)

        # refreshButton = tk.Button(self, text="Back to Home", font=SMALL_FONT,
        #                        command=lambda: self.refresh())
        # refreshButton.pack(padx=5, pady=5)

        self.is_table_deleted = False

        # Get regions, towns and flat types from datahelper
        global df
        df = dh.get_dataframe()
        towns = dh.get_all_towns()
        regions = dh.get_all_regions()
        flatTypes = dh.get_all_flatTypes()

        label = tk.Label(self, text="All the fields below are required",
                         font=NORM_FONT)
        label.pack(padx=20, pady=20)

        # Setting values for regions combo box
        listofRegions = sorted(regions)
        self.comboBoxRegion = ttk.Combobox(self, state="readonly")
        self.comboBoxRegion.pack(padx=5, pady=5)
        self.comboBoxRegion.bind('<<ComboboxSelected>>', lambda x: self.updateTownComboBox("region"))
        self.comboBoxRegion['values'] = ["Select Region"] + listofRegions
        self.comboBoxRegion.current(0)

        # Setting values for town combo box
        listofTowns = sorted(towns)
        self.comboBoxTown = ttk.Combobox(self, state="readonly")
        self.comboBoxTown.pack(padx=5, pady=5)
        self.comboBoxTown.bind('<<ComboboxSelected>>', lambda x: self.updateTownComboBox(""))
        self.comboBoxTown['values'] = ["Select Town"] + listofTowns
        self.comboBoxTown.current(0)

        # Setting values for flat types combo box
        listofFlatTypes = sorted(flatTypes)
        self.comboxBoxFlatTypes = ttk.Combobox(self, state="readonly")
        self.comboxBoxFlatTypes.pack(padx=5, pady=5)
        self.comboxBoxFlatTypes['values'] = ["Select Flat Type"] + listofFlatTypes
        self.comboxBoxFlatTypes.current(0)


        filterButton = tk.Button(self, text="Filter", font=SMALL_FONT,
                                 command=lambda: self.updateTableAfterFiltering(topframe))
        filterButton.pack(padx=10, pady=10)
        # Search results frame
        topframe = tk.Frame(self)
        topframe.pack(side=tk.TOP)


        # Plot summary table
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.table = Table(self.frame, dataframe=df)
        self.table.show()

        self.exportButton = tk.Button(self, text="Export Results", font=SMALL_FONT,
                                      command=lambda: self.displayExport())
        self.exportButton.pack(padx=10, pady=10)

    # Setting values of town combobox according to region combobox
    def updateTownComboBox(self, control):
        listofTowns = dict_input("region", self.comboBoxRegion.get())
        self.comboBoxTown['values'] = listofTowns
        self.comboBoxTown.current(0)

    def updateTableAfterFiltering(self, topframe):
        for child in topframe.winfo_children():
            child.destroy()

        # No options selected, return unfiltered table
        if self.comboBoxRegion.get() == "Select Region" or self.comboBoxTown.get() == "Select Town" or self.comboxBoxFlatTypes == "Select Flat Type":
            label = tk.Label(topframe, text="Please select an option for region, town and flat type",
                             font=VALIDAITON_FONT, fg="red")
            label.pack(padx=20, pady=20)
            self.table = Table(self.frame, dataframe=df)
            self.table.show()

        # Options selected, return filtered table
        elif not self.comboBoxRegion.get() == "Select Region" or self.comboBoxTown.get() == "Select Town" or self.comboxBoxFlatTypes == "Select Flat Type":
            resultsLabel = tk.Label(topframe, text="Your Results", font=NORM_FONT)
            resultsLabel.pack()
            # Return selected option for region
            regionLabel = tk.Label(topframe, text="Region: " + self.comboBoxRegion.get())
            regionLabel.pack()
            # Return selected option for town
            townLabel = tk.Label(topframe, text="Town: " + self.comboBoxTown.get())
            townLabel.pack()
            # Return selected option for flat type
            flatLabel = tk.Label(topframe, text="Flat Type: " + self.comboxBoxFlatTypes.get())
            flatLabel.pack()

            # Get the filter options from combobox
            filters = {"town": self.comboBoxTown.get(), "flat_type": self.comboxBoxFlatTypes.get()}

            # Replace default values to " "
            for item in filters:
                if filters[item] == "Select Town" or filters[item] == "Select Flat Type":
                    filters[item] = ""

            # Update df according to updated filtered options
            global valuesBasedOnFilters
            valuesBasedOnFilters = get_filtered_data(filters)

            # Return total number of records for search results
            global totalRecords
            totalRecords = str(len(valuesBasedOnFilters))

            totalrowsLabel = tk.Label(topframe, text="Total number of records found: " + totalRecords)
            totalrowsLabel.pack(padx=10, pady=0)

            # Repopulate table with filtered results
            if self.is_table_deleted:
                self.frame.pack()
                self.table = Table(self.frame, dataframe=valuesBasedOnFilters)
                self.table.show()
                self.exportButton.pack()
                self.is_table_deleted = False
            else:
                self.table.updateModel(TableModel(valuesBasedOnFilters))
                self.table.redraw()

            # Validation when total records is 0
            if totalRecords == "0":
                del valuesBasedOnFilters
                # self.table.clearFormatting()
                # self.table.remove()
                self.frame.pack_forget()
                self.exportButton.pack_forget()
                self.is_table_deleted = True
                validationLabel = tk.Label(topframe, text="Sorry, no matching records found based on filters. Please "
                                                          "try another search criterion.", font=VALIDAITON_FONT,
                                           fg="red")
                validationLabel.pack()

    # Export Window
    def displayExport(self):
        mainApp = ExportResults()
        mainApp.title("Export Results")
        mainApp.geometry("800x800")
        mainApp.mainloop()

    # def refresh(self):
    #     self. __init__()

app = WelcomeWindow()
app.title("HDB Resale Flats Analyser")
app.geometry("900x800")
app.mainloop()
