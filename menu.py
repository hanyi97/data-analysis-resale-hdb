import tkinter as tk
import data_helper as dh
import topNcheapest
import platform
import ctypes
import matplotlib
import search
import export
import bargraph as bg
from matplotlib.ticker import FuncFormatter
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from pandastable import Table, TableModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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
        self.create_labels()
        self.create_buttons(controller)

    def create_labels(self):
        header = tk.Label(self, text="HDB Resale Flats Analyser", font=LARGE_FONT)
        label = tk.Label(self,
                         text="This service enables you to check the resale flat prices within the last 3 years "
                              "based "
                              "on regions, "
                              "towns and flat-types.",
                         font=NORM_FONT, wraplength=450)
        header.pack(padx=0, pady=20)
        label.pack(padx=10, pady=10)

    def show_frame(self, cont):
        # show a table_frame for the given page name
        frame = self.frames[cont]  # looks for the value in self.frames with this key
        frame.tkraise()  # raises the table_frame to the front

    def create_buttons(self, controller):
        charts_btn = tk.Button(self, text="View Bar Graph", height=3, width=30, font=NORM_FONT,
                               command=lambda: controller.show_frame(ViewCharts))
        charts_btn.pack(padx=10, pady=10)

        treemap_btn = tk.Button(self, text="View Tree Map", height=3, width=30, font=NORM_FONT,
                                command=lambda: controller.show_frame(MainBrowser))
        treemap_btn.pack(pady=10, padx=10)

        summary_btn = tk.Button(self, text="View Summary", height=3, width=30, font=NORM_FONT,
                                command=lambda: controller.show_frame(ViewSummary))
        summary_btn.pack(padx=10, pady=10)

        view_top10 = tk.Button(self, text="View Top 10 Cheapest Flats", height=3, width=30, font=NORM_FONT,
                               command=lambda: controller.show_frame(ViewTop10CheapestFlats))
        view_top10.pack(padx=10, pady=10)


class ViewTop10CheapestFlats(tk.Frame):
    def __init__(self, parent, controller):
        self.is_table_deleted = False
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Top 10 Cheapest Flats", font=LARGE_FONT)
        label.pack(padx=10, pady=10)

        back_button = tk.Button(self, text="Back to Home", font=SMALL_FONT,
                                command=lambda: controller.show_frame(SelectOptions))
        back_button.pack(padx=10, pady=10)

        # Get flat types from datahelper
        self.data = dh.get_dataframe()
        flat_types = dh.get_all_flat_types()

        label = tk.Label(self, text="All the fields below are required", font=NORM_FONT)
        label.pack(padx=20, pady=20)

        # Setting values for flat types combo box
        list_of_flat_types = sorted(flat_types)
        self.combobox_flat_types = ttk.Combobox(self, state="readonly")
        self.combobox_flat_types.pack(padx=5, pady=5)
        self.combobox_flat_types['values'] = ["Select Flat Type"] + list_of_flat_types
        self.combobox_flat_types.current(0)

        filter_button = tk.Button(self, text="Filter", font=SMALL_FONT,
                                  command=lambda: self.update_table(top_frame))
        filter_button.pack(padx=10, pady=10)
        # Search results table_frame
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP)

        # Plot top10 cheapest table
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.table = Table(self.frame, dataframe=self.data, showstatusbar=True, width=1215, height=250,
                           rowselectedcolor='#83b2fc', colheadercolor='#535b71', cellbackgr='#FFF')
        self.table.show()

        # Export to PDF button
        self.export_button = tk.Button(self, text="Export Overview as PDF", font=SMALL_FONT,
                                       command=lambda: self.displayExport())
        self.export_button.pack(padx=10, pady=10)

    def update_table(self, top_frame):
        for child in top_frame.winfo_children():
            child.destroy()

        # No options selected, return unfiltered table
        if self.combobox_flat_types == "Select Flat Type":
            label = tk.Label(top_frame, text="Please select an option for flat type",
                             font=VALIDAITON_FONT, fg="red")
            label.pack(padx=20, pady=20)
            self.table = Table(self.frame, dataframe=self.data)
            self.table.show()

        # Options selected, return filtered table
        elif not self.combobox_flat_types == "Select Flat Type":
            results_label = tk.Label(top_frame, text="Your Results", font=NORM_FONT)
            results_label.pack()
            # Return selected option for flat type
            flat_label = tk.Label(top_frame, text="Flat Type: " + self.combobox_flat_types.get())
            flat_label.pack()

            # Get the filter options from combobox
            filters = {"flat_type": self.combobox_flat_types.get()}

            # Replace default values to " "
            for item in filters:
                if filters[item] == "Select Flat Type":
                    filters[item] = ""

            # Update df according to updated filtered options
            filtered_data = topNcheapest.get_cheapest_hdb(filters)

            # Return total number of records for search results
            total_records = str(len(filtered_data))

            total_rows_label = tk.Label(top_frame, text="Total number of records found: " + total_records)
            total_rows_label.pack(padx=10, pady=0)

            # Repopulate table with filtered results
            if self.is_table_deleted:
                self.frame.pack()
                self.table = Table(self.frame, dataframe=filtered_data)
                self.table.show()
                self.export_button.pack()
                self.is_table_deleted = False
            else:
                self.table.updateModel(TableModel(filtered_data))
                self.table.redraw()

            # Validation when total records is 0
            if total_records == "0":
                del filtered_data
                # self.table.clearFormatting()
                # self.table.remove()
                self.frame.pack_forget()
                self.export_button.pack_forget()
                self.is_table_deleted = True
                validation_label = tk.Label(top_frame,
                                            text="Sorry, no matching records found based on filters. Please "
                                                 "try another search criterion.", font=VALIDAITON_FONT,
                                            fg="red")
                validation_label.pack()


# Joey Function
class ViewSummary(tk.Frame):
    def __init__(self, parent, controller):
        self.is_table_deleted = False
        self.filters = {}
        self.CONST_SELECT_REGION = "Select Region"
        self.CONST_SELECT_TOWN = "Select Town"
        self.CONST_SELECT_FLAT_TYPE = "Select Flat Type"
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Overview of Resale Flats Prices", font=LARGE_FONT)
        label.grid(row=0, pady=10, padx=10)
        back_button = tk.Button(self, text="Back to Home", font=SMALL_FONT,
                                command=lambda: self.refresh(controller))
        back_button.grid(row=1, padx=5, pady=5)

        # Get regions, towns and flat types from datahelper
        self.df = dh.get_dataframe()
        self.towns = dh.get_all_towns()
        self.regions = dh.get_all_regions()
        self.flat_types = dh.get_all_flat_types()

        # label = tk.Label(self, text="Town and Flat Type are required",
        #                  font=NORM_FONT)
        # label.pack(padx=20, pady=20)

        combobox_frame = tk.Frame(self)
        combobox_frame.grid(row=2)
        # Setting values for regions combo box
        region_list = sorted(self.regions)
        self.combobox_region = ttk.Combobox(combobox_frame, state="readonly")
        # self.combobox_region.pack(side=tk.LEFT, padx=5, pady=5)
        self.combobox_region.grid(row=0, column=0, padx=5, pady=5)
        self.combobox_region.bind('<<ComboboxSelected>>', lambda x: self.update_town_combobox("region"))
        self.combobox_region['values'] = [self.CONST_SELECT_REGION] + region_list
        self.combobox_region.current(0)

        # Setting values for town combo box
        town_list = sorted(self.towns)
        self.combobox_town = ttk.Combobox(combobox_frame, state="readonly")
        # self.combobox_town.pack(side=tk.LEFT, padx=5, pady=5)
        self.combobox_town.grid(row=0, column=1, padx=5, pady=5)
        self.combobox_town.bind('<<ComboboxSelected>>', lambda x: self.town_selected(""))
        self.combobox_town['values'] = [self.CONST_SELECT_TOWN] + town_list
        self.combobox_town.current(0)

        # Setting values for flat types combo box
        flat_type_list = sorted(self.flat_types)
        self.combobox_flat_types = ttk.Combobox(combobox_frame, state="readonly")
        # self.combobox_flat_types.pack(side=tk.LEFT, padx=5, pady=5)
        self.combobox_flat_types.grid(row=0, column=2, padx=5, pady=5)
        self.combobox_flat_types['values'] = [self.CONST_SELECT_FLAT_TYPE] + flat_type_list
        self.combobox_flat_types.current(0)

        filter_button = tk.Button(combobox_frame, text="Filter", font=SMALL_FONT, width=20,
                                  command=lambda: self.update_table(self.results_frame))
        # filter_button.pack(side=tk.LEFT, padx=10, pady=10)
        filter_button.grid(row=0, column=3, padx=10, pady=10)
        # Search results table_frame
        self.results_frame = tk.Frame(self)
        self.results_frame.grid(row=3)

        # Plot summary table
        self.table_frame = tk.Frame(self)
        self.table_frame.grid(row=4)
        self.table = Table(self.table_frame, dataframe=self.df, showstatusbar=True, width=1215, height=300,
                           rowselectedcolor='#83b2fc', colheadercolor='#535b71', cellbackgr='#FFF')
        self.table.show()

        self.export_button = tk.Button(self, text="Export Results as CSV", font=SMALL_FONT,
                                       command=lambda: self.export_csv())
        self.export_button.grid(row=5, padx=10, pady=10)
        # Center widgets
        tk.Grid.rowconfigure(self, 1)
        tk.Grid.columnconfigure(self, 0, weight=1)

    # Not done
    def refresh(self, controller):
        self.combobox_region.current(0)
        self.update_town_combobox(self.combobox_region.get())
        self.combobox_flat_types.current(0)
        self.update_table(self.results_frame)
        controller.show_frame(SelectOptions)

    # Setting values of town combobox according to region combobox
    def update_town_combobox(self, control):
        town_list = search.dict_input("region", self.combobox_region.get())
        if town_list[0] != self.CONST_SELECT_TOWN:
            town_list = [self.CONST_SELECT_TOWN] + town_list
        self.combobox_town['values'] = town_list
        self.combobox_town.current(0)

    def town_selected(self, control):
        town_list = search.dict_input("region", self.combobox_region.get())
        self.combobox_town['values'] = [self.CONST_SELECT_TOWN] + town_list

    def update_table(self, frame):
        for child in frame.winfo_children():
            child.destroy()
        if not frame.winfo_ismapped():
            frame.grid(row=3)
        # # No options selected, return unfiltered table
        # if self.combobox_town.get() == "Select Town" \
        #         or self.combobox_flat_types.get() == "Select Flat Type":
        #     label = tk.Label(results_frame, text="Please select an option for town and flat type",
        #                      font=VALIDAITON_FONT, fg="red")
        #     label.pack()
        #
        #     self.table.updateModel(TableModel(self.df))
        #     self.table.redraw()
        #     if self.combobox_region.get == "Select Region":
        #         # Setting values for town combo box
        #         town_list = sorted(self.towns)
        #         self.combobox_town = ttk.Combobox(self, state="readonly")
        #         self.combobox_town.pack(padx=5, pady=5)
        #         # self.combobox_town.bind('<<ComboboxSelected>>', lambda x: self.update_town_combobox(""))
        #         self.combobox_town['values'] = town_list
        #         self.combobox_town.current(0)
        # # Options selected, return filtered table
        # else:
        selected_region = self.combobox_region.get()
        selected_town = self.combobox_town.get()
        selected_flat_type = self.combobox_flat_types.get()
        if selected_region == self.CONST_SELECT_REGION and selected_town == self.CONST_SELECT_TOWN \
                and selected_flat_type == self.CONST_SELECT_FLAT_TYPE:
            frame.grid_forget()

        results_label = tk.Label(frame, text="Your Results", font=NORM_FONT)
        results_label.pack()
        if selected_region != self.CONST_SELECT_REGION:
            # Return selected option for region
            region_label = tk.Label(frame, text="Region: " + selected_region)
            region_label.pack()
        if selected_town != self.CONST_SELECT_TOWN:
            # Return selected option for town
            town_label = tk.Label(frame, text="Town: " + selected_town)
            town_label.pack()
        if selected_flat_type != self.CONST_SELECT_FLAT_TYPE:
            # Return selected option for flat type
            flat_label = tk.Label(frame, text="Flat Type: " + selected_flat_type)
            flat_label.pack()

        # Get the filter options from combobox
        self.filters = {"region": selected_region, "town": selected_town, "flat_type": selected_flat_type}

        # Remove item from dict if default selection
        for item in list(self.filters):
            if self.filters[item] == self.CONST_SELECT_REGION or self.filters[item] == self.CONST_SELECT_TOWN \
                    or self.filters[item] == self.CONST_SELECT_FLAT_TYPE:
                del self.filters[item]

        # Update df according to updated filtered options
        filtered_data = search.get_filtered_data(self.filters)

        # Return total number of records for search results
        total_records = str(len(filtered_data))
        total_rows_label = tk.Label(frame, text="Total number of records found: " + total_records)
        total_rows_label.pack(padx=10, pady=0)

        # Repopulate table with filtered results
        if self.is_table_deleted:
            self.table_frame.grid(row=4)
            self.table = Table(self.table_frame, showstatusbar=True, width=1215, height=300,
                               rowselectedcolor='#83b2fc', colheadercolor='#535b71', cellbackgr='#FFF')
            self.table.show()
            self.export_button.grid(row=5)
            self.is_table_deleted = False
        self.table.updateModel(TableModel(filtered_data))
        self.table.redraw()

        # Validation when total records is 0
        if total_records == "0":
            del filtered_data
            self.table_frame.grid_forget()
            self.export_button.grid_forget()
            self.is_table_deleted = True
            validation_label = tk.Label(frame,
                                        text="Sorry, no matching records found based on filters. Please "
                                             "try another search criterion.", font=VALIDAITON_FONT,
                                        fg="red")
            validation_label.pack()

    # Export Window
    def export_csv(self):
        file = asksaveasfile(filetypes=[('CSV Files', '*.csv')], defaultextension=[('CSV Files', '*.csv')],
                             initialfile='summary.csv')
        if file is not None:
            export.export_to_csv(file.name, self.filters)


class ViewCharts(tk.Frame):
    def plot_bar_graph(self, town=''):
        try:
            if town == 'Select Town':
                town = ''
            town = town.upper()
            df = bg.get_filtered_data(town)
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
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
        except AttributeError:
            pass

        # Add the bar graph into the ViewCharts window
        self.canvas = FigureCanvasTkAgg(self.plot_bar_graph(self.town_combobox.get()), master=self)

        # to display toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def refresh(self, controller):
        self.town_combobox.current(0)
        self.selected('')
        controller.show_frame(SelectOptions)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = None
        self.toolbar = None
        label = tk.Label(self, text="Analyse Resale Flats by Town", font=NORM_FONT)
        label.pack(padx=10, pady=10)

        back_button = tk.Button(self, text="Back to Home", font=SMALL_FONT,
                                command=lambda: self.refresh(controller))
        back_button.pack()

        # Add dropdown list with list of towns:
        town_list_options = dh.get_all_towns()
        clicked = tk.StringVar()
        clicked.set(town_list_options[0])

        # Add Combobox with the list of towns onto the GUI:
        self.town_combobox = ttk.Combobox(self, value=["Select Town"] + town_list_options, state='readonly')
        self.town_combobox.current(0)
        self.town_combobox.bind("<<ComboboxSelected>>", self.selected)
        self.town_combobox.pack(pady=10)

        # Initialise default bar graph
        self.selected('')


class MainBrowser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.focus_set()
        self.bind("<Configure>", self.on_configure)

        back_button = tk.Button(self, text="Back to Home", font=SMALL_FONT,
                                command=lambda: controller.show_frame(SelectOptions))
        back_button.grid(row=0, column=0, pady=10)

        # Browser
        self.browser_frame = Browser(self, controller)
        self.browser_frame.grid(row=1, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

    def on_configure(self, event):
        if self.browser_frame:
            self.browser_frame.on_mainframe_configure(event.width, event.height)

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


if __name__ == "__main__":
    app = WelcomeWindow()
    app.title("HDB Resale Flats Analyser")
    width, height = app.winfo_screenwidth(), app.winfo_screenheight()  # Retrieve screen size
    app.geometry("%dx%d" % (width, height))  # Set full screen with tool bar on top
    # cef.Initialize()
    app.mainloop()
    # cef.Shutdown()
