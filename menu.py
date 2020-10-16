import tkinter as tk
from tkinter import ttk

from display_data import *
from search import *
from data_helper import *

from pandastable import Table
import bargraph
import matplotlib


matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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

        for F in (SelectOptions, ViewCharts, ViewSummary, View10Top):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(SelectOptions)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Selection Window
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


# Top10 Window
class Top10Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = View10Top(container, self)
        self.frames[View10Top] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(View10Top)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


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

        df = data_helper.get_dataframe()

        columns = data_helper.get_columnname()
        print(columns)
        towns = data_helper.get_all_towns()
        regions = data_helper.get_all_regions()
        flatTypes = data_helper.get_all_flatTypes()
        print(towns)
        print(regions)
        print(flatTypes)

        # Setting values for regions combo box
        listofRegions = sorted(regions)
        self.comboBoxRegion = ttk.Combobox(self, state="readonly")
        self.comboBoxRegion.pack(pady=0, padx=0)
        self.comboBoxRegion.bind('<<ComboboxSelected>>', lambda x: self.updateTable("region"))
        self.comboBoxRegion['values'] = listofRegions
        self.comboBoxRegion.current(0)


        # Setting values for town combo box
        listofTowns = sorted(towns)
        self.comboBoxTown = ttk.Combobox(self, state="readonly")
        self.comboBoxTown.pack(pady=0, padx=0)
        self.comboBoxTown.bind('<<ComboboxSelected>>', lambda x: self.updateTable(""))
        self.comboBoxTown['values'] = listofTowns
        self.comboBoxTown.current(0)

        # Setting values for flat types combo box
        listofFlatTypes = sorted(flatTypes)
        self.comboxBoxFlatTypes = ttk.Combobox(self, state="readonly")
        self.comboxBoxFlatTypes.pack(pady=0, padx=0)
        # self.comboBoxRegion.bind('<<ComboboxSelected>>', lambda x: self.updateGraph(csvPath, "company"))
        self.comboxBoxFlatTypes['values'] = listofFlatTypes
        self.comboxBoxFlatTypes.current(0)



        # df = df.sort_values(by=['year', 'month'])  # sort dataframe in ascending chronological order

        #creating summary table
        frame = Frame(self)
        frame.pack()
        self.table = Table(frame, dataframe=df,
                      height=400, width=1100)
        self.table.show()

    #     top10button = tk.Button(self, text="View Top 10", font=SMALL_FONT,
    #                             command=lambda: self.displayTop10())
    #     top10button.pack(padx=10, pady=10)
    #
    # def displayTop10(self):
    #     mainApp = Top10Window()
    #     mainApp.title("Top 10 Resale Flats")
    #     mainApp.geometry("900x900")
    #     mainApp.mainloop()

    def updateTable(self, control):

        if control == "region":
            #resets town dropdown based on region
            listofTowns = get_town_acrd_region(self.comboBoxRegion.get())
            self.comboBoxTown['values'] = listofTowns
            self.comboBoxTown.current(0)


        valuesBasedOnTowns= get_filtered_data(self.comboBoxRegion.get())
        print("region", valuesBasedOnTowns)
        # valuesBasedOnTowns = get_filtered_data(self.comboBoxTown.get())
        # print("town", valuesBasedOnTowns)
        # valuesBasedOnFlats = get_filtered_data(self.comboxBoxFlatTypes.get())
        # print("flat types", valuesBasedOnFlats)


        # clear existing data in table



# Kah En Function
class View10Top(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Top 10 Resale Flats Prices", font=NORM_FONT)
        label.pack(pady=10, padx=10)


app = WelcomeWindow()
app.title("HDB Resale Flats Analyser")
app.geometry("600x600")
app.mainloop()
#
# if __name__ == "__main__":
#     class WelcomeWindow(tk.Tk):
#         def __init__(self, *args, **kwargs):
#             tk.Tk.__init__(self, *args, **kwargs)
#             container = tk.Frame(self)
#             container.pack(side="top", fill="both", expand=True) #fill will fill in the space that the pack has been allotted to. expand will fill up the rest of the white space
#             container.grid_rowconfigure(0, weight=1) #0 is the minimum size, weight is priority
#             container.grid_columnconfigure(0, weight=1)
#             self.frames = {}
#
#             # all pages must be included in this dictionary in order to be raised to the top (accessed)
#             for F in (SelectOptions, ViewCharts, ViewSummary):
#                 frame = F(container, self)
#
#                 self.frames[F] = frame
#
#                 # put all of the pages in the same location;
#                 # the one on the top of the stacking order
#                 # will be the one that is visible.
#                 frame.grid(row=0, column=0, sticky="nsew") #sticky will stretch everything to the size of the window
#             self.show_frame(SelectOptions)
#
#         def show_frame(self, cont):
#             # show a frame for the given page name
#             frame = self.frames[cont] #looks for the value in self.frames with this key
#             frame.tkraise() #raises the frame to the front
#
#
#     class SelectOptions(tk.Frame):
#         def __init__(self, parent, controller):
#             #self --> current object
#             #parent --> a widget to act as the parent of the current object. All widgets in tkinter except the root window require a parent (sometimes also called a master)
#             #controller -->some other object that is designed to act as a common point of interaction for several pages of widgets
#
#             tk.Frame.__init__(self, parent) #parent --> parent class (WelcomeWindow)
#             self.createLabels()
#             self.createButtons(controller)
#
#         def createLabels(self):
#             header = tk.Label(self,text="HDB Resale Flats Analyser", font=LARGE_FONT) #created the header object
#             label = tk.Label(self,
#                 text="This service enables you to check the resale flat prices within the last 3 years based on regions, "
#                      "towns and flat-types.",
#                 font=SMALL_FONT, wraplength=450)
#             header.pack(padx=0, pady=20) #pack is to place it on the page. padx or pady -> horizontal/vertical internal padding.
#             label.pack(padx=10, pady=10)
#
#         def createButtons(self, controller):
#             #lambda creates a throwaway function that will only be here when it is called.
#             #it cannot be used to pass parameters through
#             # shows the ViewCharts class page upon clicking the button
#             chartsBTN = tk.Button(self, text="View Charts", height=5, width=30, font=SMALL_FONT,
#                                   command=lambda: controller.show_frame(ViewCharts))
#             chartsBTN.pack(pady=10, padx=10)
#
#             # shows the ViewSummary class page upon clicking the button
#             summaryBTN = tk.Button(self, text="View Summary", height=5, width=30, font=SMALL_FONT,
#                                    command=lambda: controller.show_frame(ViewSummary))
#             summaryBTN.pack()
#
#     # Setting up the ViewCharts page
#     class ViewCharts(tk.Frame):
#         def __init__(self, parent, controller):
#             tk.Frame.__init__(self, parent)
#             label = tk.Label(self, text="Analyse Resale Flats by Region", font=NORM_FONT)
#             label.pack(padx=10, pady=10)
#
#             # Adds the graph from bargraph.py into the ViewCharts windwo
#             canvas = FigureCanvasTkAgg(bargraph.plot_bar_graph(), master=self)
#             canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
#
#             backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
#             backbutton.pack(padx=10, pady=10)
#
#     # Setting up the ViewSummary page
#     class ViewSummary(tk.Frame):
#         def __init__(self, parent, controller):
#             tk.Frame.__init__(self, parent)
#             label = tk.Label(self, text="Resale Flats Summary", font=NORM_FONT)
#             label.pack(pady=10, padx=10)
#
#             backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
#             backbutton.pack()
#
#
#     app = WelcomeWindow()
#     app.title("HDB Resale Flats Analyser") #sets title of window
#     app.geometry("1920x1080") #sets dimensions of tkinter window
#     app.mainloop() #infinite loop so that events get processed
