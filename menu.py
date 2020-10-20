import tkinter as tk
import data_helper as dh
import topNcheapest
import platform
import ctypes
import matplotlib
from matplotlib.ticker import FuncFormatter
from tkinter import ttk
from search import *
from pandastable import Table, TableModel
from bargraph import get_filtered_data
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from cefpython3 import cefpython as cef
from numpy import arange
from matplotlib.figure import Figure

matplotlib.use("TkAgg")

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Reusable font sizes
LARGE_FONT = ("Open Sans", 30)
NORM_FONT = ("Open Sans", 16)
SMALL_FONT = ("Open Sans", 15)
VALIDAITON_FONT = ("Open Sans", 12)

CONST_FILE_PATH = "resources/bargraph.png"

if __name__ == "__main__":
    # Main Window
    class WelcomeWindow(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
            self.frames = {}
            for F in (SelectOptions, ViewCharts, ViewSummary, MainBrowser, ViewTop10CheapestFlats):
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
            # self --> current object
            # parent --> a widget to act as the parent of the current object. All widgets in
            # tkinter except the root window require a parent (sometimes also called a master)
            # controller -->some
            # other object that is designed to act as a common point of interaction for several pages of widgets
            tk.Frame.__init__(self, parent)
            self.createLabels()
            self.createButtons(controller)

        def createLabels(self):
            header = tk.Label(self, text="HDB Resale Flats Analyser", font=LARGE_FONT)
            label = tk.Label(self,
                             text="This service enables you to check the resale flat prices within the last 3 years "
                                  "based "
                                  "on regions, "
                                  "towns and flat-types.",
                             font=NORM_FONT, wraplength=450)
            header.pack(padx=0, pady=20)
            label.pack(padx=10, pady=10)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            # self.frame.grid(row=0, column=0, sticky="nsew")  # sticky will stretch everything to the size of the window
            # self.show_frame(SelectOptions)

        def show_frame(self, cont):
            # show a frame for the given page name
            frame = self.frames[cont]  # looks for the value in self.frames with this key
            frame.tkraise()  # raises the frame to the front

        def createButtons(self, controller):
            chartsBTN = tk.Button(self, text="View Charts", height=5, width=30, font=NORM_FONT,
                                  command=lambda: controller.show_frame(ViewCharts))
            chartsBTN.pack(padx=10, pady=10)

            treemapBTN = tk.Button(self, text="View Tree Map", height=5, width=30, font=NORM_FONT,
                                   command=lambda: controller.show_frame(MainBrowser))
            treemapBTN.pack(pady=10, padx=10)

            summaryBTN = tk.Button(self, text="View Summary", height=5, width=30, font=NORM_FONT,
                                   command=lambda: controller.show_frame(ViewSummary))
            summaryBTN.pack(padx=10, pady=10)

            ViewTop10 = tk.Button(self, text="View Top 10 Cheapest Flats", height=5, width=30, font=NORM_FONT,
                                  command=lambda: controller.show_frame(ViewTop10CheapestFlats))
            ViewTop10.pack(padx=10, pady=10)

    # Export Data Window
    class ExportResults(tk.Frame):
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

    class ViewTop10CheapestFlats(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="Top 10 Cheapest Flats", font=LARGE_FONT)
            label.pack(padx=10, pady=10)

            backbutton = tk.Button(self, text="Back to Home", font=SMALL_FONT,
                                   command=lambda: controller.show_frame(SelectOptions))
            backbutton.pack(padx=10, pady=10)

            self.is_table_deleted = False

            # Get flat types from datahelper
            global df
            df = dh.get_dataframe()
            flatTypes = dh.get_all_flatTypes()

            label = tk.Label(self, text="All the fields below are required",
                             font=NORM_FONT)
            label.pack(padx=20, pady=20)

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

            # Plot top10 cheapest table
            self.frame = tk.Frame(self)
            self.frame.pack()
            self.table = Table(self.frame, dataframe=df, showstatusbar=True, width=1000)
            self.table.show()

        def updateTableAfterFiltering(self, topframe):
            for child in topframe.winfo_children():
                child.destroy()

            # No options selected, return unfiltered table
            if self.comboxBoxFlatTypes == "Select Flat Type":
                label = tk.Label(topframe, text="Please select an option for flat type",
                                 font=VALIDAITON_FONT, fg="red")
                label.pack(padx=20, pady=20)
                self.table = Table(self.frame, dataframe=df)
                self.table.show()

            # Options selected, return filtered table
            elif not self.comboxBoxFlatTypes == "Select Flat Type":
                resultsLabel = tk.Label(topframe, text="Your Results", font=NORM_FONT)
                resultsLabel.pack()
                # Return selected option for flat type
                flatLabel = tk.Label(topframe, text="Flat Type: " + self.comboxBoxFlatTypes.get())
                flatLabel.pack()

                # Get the filter options from combobox
                filters = {"flat_type": self.comboxBoxFlatTypes.get()}

                # Replace default values to " "
                for item in filters:
                    if filters[item] == "Select Flat Type":
                        filters[item] = ""

                # Update df according to updated filtered options
                global valuesBasedOnFilters
                valuesBasedOnFilters = topNcheapest.get_filtered_data(filters)

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
                    validationLabel = tk.Label(topframe,
                                               text="Sorry, no matching records found based on filters. Please "
                                                    "try another search criterion.", font=VALIDAITON_FONT,
                                               fg="red")
                    validationLabel.pack()

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
            self.table = Table(self.frame, dataframe=df, showstatusbar=True, width=1000)
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
                    self.table = Table(self.frame)
                    self.table.show()
                    self.exportButton.pack()
                    self.is_table_deleted = False
                else:
                    self.table.updateModel(TableModel(valuesBasedOnFilters))
                    self.table.redraw()

                # Validation when total records is 0
                if totalRecords == "0":
                    del valuesBasedOnFilters
                    self.frame.pack_forget()
                    self.exportButton.pack_forget()
                    self.is_table_deleted = True
                    validationLabel = tk.Label(topframe,
                                               text="Sorry, no matching records found based on filters. Please "
                                                    "try another search criterion.", font=VALIDAITON_FONT,
                                               fg="red")
                    validationLabel.pack()

        # Export Window
        def displayExport(self):
            mainApp = ExportResults()
            mainApp.title("Export Results")
            mainApp.geometry("800x800")
            mainApp.mainloop()


    class ViewCharts(tk.Frame):
        def plot_bar_graph(self, town=''):
            try:
                town = town.upper()
                df = get_filtered_data(town)
                if len(df) == 0:
                    raise IndexError("No data found!")
                # Set town to Singapore when no town is selected
                town = 'SINGAPORE' if town == '' else town

                # Create a figure
                fig = Figure(figsize=(20, 5))
                ax = fig.add_subplot(111)
                # Bar graph configuration
                bargraph = df.plot.barh(color='#24AEDE', ax=ax, zorder=2, label='Average Resale Pricing')
                # Set x ticks to frequency of 100,000
                start, end = bargraph.get_xlim()
                bargraph.xaxis.set_ticks(arange(start, end, 100000))
                # Add comma to resale flat prices
                bargraph.get_xaxis().set_major_formatter(FuncFormatter(lambda x, loc: '{:,}'.format(int(x))))
                # Remove borders
                bargraph.spines['right'].set_visible(False)
                bargraph.spines['top'].set_visible(False)
                bargraph.spines['left'].set_visible(False)
                bargraph.spines['bottom'].set_visible(False)
                # Draw vertical axis lines
                ticks = ax.get_xticks()
                for tick in ticks:
                    bargraph.axvline(x=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)
                # Set average resale value to bar labels
                for i in bargraph.patches:
                    price = i.get_width()
                    bargraph.text(price + .3, i.get_y() + .15, str(" ${:,}".format(int(price))),
                                  fontsize=10,
                                  color='dimgrey')
                # Style labels and title
                label_style = {'fontsize': 10, 'fontweight': 'heavy'}
                bargraph.set_xlabel('Average Resale Value (SGD)',
                                    fontdict=label_style)
                bargraph.set_ylabel('HDB Flat Type',
                                    fontdict=label_style)
                bargraph.set_title('Town: (%s)\nAverage HDB resale value by flat type' % town,
                                   fontdict={'fontsize': 12, 'fontweight': 'heavy'})
                bargraph.legend(loc="lower right", bbox_to_anchor=(1., 1.02), borderaxespad=0.)
                # Save bar graph as png
                bargraph.get_figure().savefig(CONST_FILE_PATH, bbox_inches='tight', dpi=300)

                return fig
            except ValueError:
                print('Cannot convert data to an integer!')
            except IndexError as e:
                print(e)

        # Run this function when user selects from the dropdown list
        def selected(self, event):
            # Clear the previous chart & toolbar first if it is currently on the screen
            try:
                self.canvas.get_tk_widget().pack_forget()
                self.toolbar.pack_forget()
            except AttributeError:
                pass

            # Add the bargraph into the ViewCharts window
            self.canvas = FigureCanvasTkAgg(self.plot_bar_graph(self.town_combobox.get()), master=self)

            # to display toolbar
            self.toolbar = NavigationToolbar2Tk(self.canvas, self)
            self.toolbar.update()

            self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)

            label = tk.Label(self, text="Analyse Resale Flats by Region", font=NORM_FONT)
            label.pack(padx=10, pady=10)

            # Add dropdown list with list of towns:
            town_list_options = data_helper.get_all_towns()
            clicked = tk.StringVar()
            clicked.set(town_list_options[0])

            # Add Combobox with the list of towns onto the GUI:
            self.town_combobox = ttk.Combobox(self, value=town_list_options)
            self.town_combobox.current(0)
            self.town_combobox.bind("<<ComboboxSelected>>", self.selected)
            self.town_combobox.pack()

            backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
            backbutton.pack(padx=10, pady=10)


    class MainBrowser(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.focus_set()
            self.bind("<Configure>", self.on_configure)

            backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
            backbutton.grid(row=0, column=0, pady=10)

            # Browser
            self.browser_frame = Browser(self, controller)
            self.browser_frame.grid(row=1, column=0,
                                    sticky=(tk.N + tk.S + tk.E + tk.W))
            tk.Grid.rowconfigure(self, 1, weight=1)
            tk.Grid.columnconfigure(self, 0, weight=1)

        def on_configure(self, event):
            if self.browser_frame:
                width = event.width
                height = event.height
                self.browser_frame.on_mainframe_configure(width, height)

        def get_browser(self):
            if self.browser_frame:
                return self.browser_frame.browser
            return None

        def get_browser_frame(self):
            if self.browser_frame:
                return self.browser_frame
            return None


    class Browser(tk.Frame):
        def __init__(self, parent, controller):
            self.browser = None
            tk.Frame.__init__(self, parent)
            self.bind("<FocusIn>", self.on_focus_in)
            self.bind("<FocusOut>", self.on_focus_out)
            self.bind("<Configure>", self.on_configure)
            self.focus_set()

        def embed_browser(self):
            window_info = cef.WindowInfo()
            rect = [0, 0, self.winfo_width(), self.winfo_height()]
            v = tk.StringVar()
            v.set("https://chart-studio.plotly.com/~si00/1.embed")
            window_info.SetAsChild(self.get_window_handle(), rect)
            self.browser = cef.CreateBrowserSync(window_info, url="https://chart-studio.plotly.com/~si00/1.embed",
                                                 window_title="Tree Map")
            assert self.browser
            self.browser.SetClientHandler(LoadHandler(self))
            self.message_loop_work()

        def get_window_handle(self):
            if self.winfo_id() > 0:
                return self.winfo_id()
            else:
                raise Exception("Couldn't obtain window handle")

        def message_loop_work(self):
            cef.MessageLoopWork()
            self.after(10, self.message_loop_work)

        def on_focus_in(self, _):
            if self.browser:
                self.browser.SetFocus(True)

        def on_focus_out(self, _):
            if self.browser:
                self.browser.SetFocus(False)

        def on_configure(self, _):
            if not self.browser:
                self.embed_browser()

        def on_mainframe_configure(self, width, height):
            if self.browser:
                if WINDOWS:
                    ctypes.windll.user32.SetWindowPos(
                        self.browser.GetWindowHandle(), 0,
                        0, 0, width, height, 0x0002)
                elif LINUX:
                    self.browser.SetBounds(0, 0, width, height)
                self.browser.NotifyMoveOrResizeStarted()


    class LoadHandler(object):
        def __init__(self, browser_frame):
            self.browser_frame = browser_frame


app = WelcomeWindow()
app.title("HDB Resale Flats Analyser")
app.geometry("1920x1080")
cef.Initialize()
app.mainloop()
cef.Shutdown()
app.mainloop()
# root = tk.Tk
# root.attributes('-fullscreen', True)
