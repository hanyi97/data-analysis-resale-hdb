import tkinter as tk
import data_helper as dh
import platform
import ctypes
import matplotlib
import filter
import export
import bargraph as bg
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from pandastable import Table, TableModel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from cefpython3 import cefpython as cef

matplotlib.use('TkAgg')

# Platforms
WINDOWS = (platform.system() == 'Windows')
LINUX = (platform.system() == 'Linux')
MAC = (platform.system() == 'Darwin')

# Reusable font sizes
LARGE_FONT = ('Roboto', 30, 'bold')
HEADER_FONT = ('Roboto', 23, 'bold')
NORM_FONT = ('Roboto', 16)
BUTTON_FONT = ('Roboto', 14, 'bold')
SMALL_FONT = ('Roboto', 15)
VALIDAITON_FONT = ('Roboto', 12)
# RESULTS_LABEL_FONT = ('Roboto', 10, 'bold')

CONST_FILE_PATH = 'resources/bargraph.png'
filters = {}


def rename_columns(df):
    df.columns = list(map(lambda col_name: col_name.upper().replace('_', ' '), df.columns))


class WelcomeWindow(tk.Tk):
    """Welcome window is the main window
       """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (SelectOptions, ViewSummary, AverageByRegion, AverageByFlatType):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(SelectOptions)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class SelectOptions(tk.Frame):
    """Users can to select their preferred option in main menu.
           Options include Overview of resale flat prices, Average resale based on regions, Average resale prices based on flat types
       """

    def __init__(self, parent, controller):
        # self --> current object
        # parent --> a widget to act as the parent of the current object. All widgets in
        # tkinter except the root window require a parent (sometimes also called a master)
        # controller -->some
        # other object that is designed to act as a common point of interaction for several pages of widgets
        root = tk.Frame.__init__(self, parent)
        self.create_labels()
        self.create_buttons(controller)
        # win= tk.Tk()
        # bgImage = tk.PhotoImage(file='singapore-flats-M9ZQMUG.ppm')
        # tk.Label(win, image=bgImage).place(relwidth=1, relheight=1)

    def create_labels(self):
        header = tk.Label(self, text='HDB Resale Flats Analyser', font=LARGE_FONT)
        label = tk.Label(self,
                         text='This service enables you to check the resale flat prices within the last 3 years '
                              'based '
                              'on regions, '
                              'towns and flat-types.',
                         font=NORM_FONT, wraplength=700)
        header.pack(padx=0, pady=30)
        label.pack(padx=0, pady=10)

    def show_frame(self, cont):
        # show a table_frame for the given page name
        frame = self.frames[cont]  # looks for the value in self.frames with this key
        frame.tkraise()  # raises the table_frame to the front

    def create_buttons(self, controller):
        overview_btn = tk.Button(self, text='Overview of resale flat prices', height=3, width=45, font=BUTTON_FONT,
                                 background='#007C89', fg="white", cursor="hand2",
                                 command=lambda: controller.show_frame(ViewSummary))
        overview_btn.pack(padx=10, pady=10)

        avgbyregion_btn = tk.Button(self, text='Average resale prices based on regions', height=3, width=45,
                                    font=BUTTON_FONT, background='#007C89', fg="white", cursor="hand2",
                                    command=lambda: controller.show_frame(AverageByRegion))
        avgbyregion_btn.pack(pady=10, padx=10)

        avgbyflattype_btn = tk.Button(self, text='Average resale prices based on flat types', height=3, width=45,
                                      font=BUTTON_FONT, background='#007C89', fg="white", cursor="hand2",
                                      command=lambda: controller.show_frame(AverageByFlatType))
        avgbyflattype_btn.pack(padx=10, pady=10)


class ViewTop10CheapestFlatsWindow(tk.Tk):
    """This window is a separate pop up that is triggered when user clicks on View Top 10 in Overview of Resale Flats Prices window.
         """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frame = ViewTop10CheapestFlats(container, self)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.tkraise()


class ViewTop10CheapestFlats(tk.Frame):
    """Top 10 Cheapest Flats table will be populated according to what user filtered in the previous window.
       User can filter top 10 according to the flat type.
       """

    def __init__(self, parent, controller):
        self.is_table_deleted = False
        self.CONST_SELECT_FLAT_TYPE = 'Select Flat Type'
        tk.Frame.__init__(self, parent)
        # Create screen title
        label = tk.Label(self, text='Top 10 Cheapest Flats', font=NORM_FONT)
        label.grid(row=0, padx=10, pady=10)

        # Get flat types from datahelper
        self.data = filter.get_cheapest_hdb(filters)
        rename_columns(self.data)
        flat_types = dh.get_all_flat_types()

        # If user did not filter flat type, show combobox
        if 'flat_type' not in filters:
            combobox_frame = tk.Frame(self)
            combobox_frame.grid(row=2)
            # Setting values for flat types combo box
            self.combobox_flat_types = ttk.Combobox(combobox_frame, state='readonly')
            self.combobox_flat_types.grid(row=0, column=0, padx=5, pady=5)
            self.combobox_flat_types['values'] = [self.CONST_SELECT_FLAT_TYPE] + flat_types
            self.combobox_flat_types.current(0)
            # Create filter button
            filter_button = tk.Button(combobox_frame, text='Filter', font=BUTTON_FONT, width=20,
                                      background='#DBD9D2', cursor='hand2', foreground='black',
                                      command=lambda: self.update_table(results_frame))
            filter_button.grid(row=0, column=1, padx=10, pady=10)

        # Search results table_frame
        results_frame = tk.Frame(self)
        results_frame.grid(row=3)

        # Plot top10 cheapest table
        self.table_frame = tk.Frame(self)
        self.table_frame.grid(row=4)
        self.table = Table(self.table_frame, dataframe=self.data, width=1215, height=300,
                           rowselectedcolor='#F6F6F4', colheadercolor='#007C89', cellbackgr='#FFFFFF', cellwidth=80,
                           rowheight=30)
        self.table.show()
        # Export to PDF button
        self.export_button = tk.Button(self, text='Export Cheapest Flats as PDF', font=BUTTON_FONT,
                                       background='#007C89',
                                       foreground="white", cursor='hand2',
                                       command=lambda: self.export_pdf())
        self.export_button.grid(row=5, padx=10, pady=10)

        # Center widgets
        tk.Grid.rowconfigure(self, 1)
        tk.Grid.columnconfigure(self, 0, weight=1)

    def update_table(self, frame):
        for child in frame.winfo_children():
            child.destroy()
        if not frame.winfo_ismapped():
            frame.grid(row=3)
        # Options selected, return filtered table
        if self.combobox_flat_types.get() != self.CONST_SELECT_FLAT_TYPE:
            results_label = tk.Label(frame, text='Your Results', font=NORM_FONT)
            results_label.pack()
            # Return selected option for flat type
            flat_label = tk.Label(frame, text='Flat Type: ' + self.combobox_flat_types.get())
            flat_label.pack()
        else:
            frame.grid_forget()

        global filters
        filters['flat_type'] = self.combobox_flat_types.get()
        for item in list(filters):
            if filters[item] == self.CONST_SELECT_FLAT_TYPE:
                del filters[item]

        # Update df according to updated filtered options
        filtered_data = filter.get_cheapest_hdb(filters)
        rename_columns(filtered_data)
        # Return total number of records for search results
        total_records = str(len(filtered_data))

        # Display Total records when option selected
        if self.combobox_flat_types.get() != self.CONST_SELECT_FLAT_TYPE:
            total_rows_label = tk.Label(frame, text='Total number of records found: ' + total_records)
            total_rows_label.pack(padx=10, pady=0)

        # Repopulate table with filtered results
        if self.is_table_deleted:
            self.table_frame.grid(row=4)
            self.table = Table(self.table_frame, dataframe=filtered_data, width=1150, height=250,
                               rowselectedcolor='#83b2fc', colheadercolor='#535b71', cellbackgr='#FFF')
            self.table.show()
            self.export_button.grid(row=5)
            self.is_table_deleted = False
        self.table.updateModel(TableModel(filtered_data))
        self.table.redraw()

        # Validation when total records is 0
        if total_records == '0':
            del filtered_data
            self.table_frame.grid_forget()
            self.export_button.grid_forget()
            self.is_table_deleted = True
            validation_label = tk.Label(frame,
                                        text='Sorry, no matching records found based on filters. Please '
                                             'try another search criterion.', font=VALIDAITON_FONT,
                                        fg='red')
            validation_label.pack()

    # Export Window
    @staticmethod
    def export_pdf():
        file = asksaveasfile(filetypes=[('pdf file', '*.pdf')], defaultextension=[('pdf file', '*.pdf')],
                             initialfile='Top10CheapestResaleFlats.pdf')
        if file is not None:
            export.export_to_pdf(file.name, filters)


class ViewSummary(tk.Frame):
    """Overview of resale flat prices where users can filter results based on region, town, flat type.
       """

    def __init__(self, parent, controller):
        self.is_table_deleted = False
        self.CONST_SELECT_REGION = 'Select Region'
        self.CONST_SELECT_TOWN = 'Select Town'
        self.CONST_SELECT_FLAT_TYPE = 'Select Flat Type'
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Overview of Resale Flats Prices', font=HEADER_FONT)
        label.grid(row=0, padx=0, pady=30)

        back_button = tk.Button(self, text='Back to Home', font=BUTTON_FONT, background='#007C89', foreground="white",
                                cursor='hand2',
                                command=lambda: self.refresh(controller))
        back_button.grid(row=1, padx=0, pady=10)

        # Get regions, towns and flat types from datahelper
        self.df = dh.get_dataframe()
        rename_columns(self.df)
        self.towns = dh.get_all_towns()
        self.regions = dh.get_all_regions()
        self.flat_types = dh.get_all_flat_types()

        combobox_frame = tk.Frame(self)
        combobox_frame.grid(row=2)
        # Setting values for regions combo box
        region_list = sorted(self.regions)
        self.combobox_region = ttk.Combobox(combobox_frame, state='readonly')
        self.combobox_region.grid(row=0, column=0, padx=5, pady=5)
        self.combobox_region.bind('<<ComboboxSelected>>', lambda x: self.update_town_combobox('region'))
        self.combobox_region['values'] = [self.CONST_SELECT_REGION] + region_list
        self.combobox_region.current(0)

        # Setting values for town combo box
        town_list = sorted(self.towns)
        self.combobox_town = ttk.Combobox(combobox_frame, state='readonly')
        # self.combobox_town.pack(side=tk.LEFT, padx=5, pady=5)
        self.combobox_town.grid(row=0, column=1, padx=5, pady=5)
        self.combobox_town.bind('<<ComboboxSelected>>', lambda x: self.town_selected(''))
        self.combobox_town['values'] = [self.CONST_SELECT_TOWN] + town_list
        self.combobox_town.current(0)

        # Setting values for flat types combo box
        flat_type_list = sorted(self.flat_types)
        self.combobox_flat_types = ttk.Combobox(combobox_frame, state='readonly')
        self.combobox_flat_types.grid(row=0, column=2, padx=5, pady=5)
        self.combobox_flat_types['values'] = [self.CONST_SELECT_FLAT_TYPE] + flat_type_list
        self.combobox_flat_types.current(0)

        filter_button = tk.Button(combobox_frame, text='Filter', font=BUTTON_FONT, width=20,
                                  background='#DBD9D2', cursor='hand2', foreground='black',
                                  command=lambda: self.update_table(self.results_frame))
        filter_button.grid(row=0, column=3, padx=10, pady=10)

        # Search results table_frames
        self.results_frame = tk.Frame(self)
        self.results_frame.grid(row=3)

        self.export_button = tk.Button(self, text='Export', font=BUTTON_FONT, background='#007C89', foreground="white",
                                       cursor='hand2',
                                       command=lambda: self.export_csv())
        self.export_button.grid(row=5, padx=0, pady=20)

        # Plot summary table
        self.table_frame = tk.Frame(self)
        self.table_frame.grid(row=4)
        self.table = Table(self.table_frame, dataframe=self.df, showstatusbar=True, width=1215, height=300,
                           rowselectedcolor='#F6F6F4', colheadercolor='#007C89', cellbackgr='#FFFFFF', cellwidth=80,
                           rowheight=30)
        self.table.show()

        self.top10_button = tk.Button(self, text='View Top 10 Cheapest Flats', font=BUTTON_FONT, background='#DBD9D2',
                                      foreground="black", cursor='hand2',
                                      command=lambda: self.show_top10())
        self.top10_button.grid(row=6, padx=0, pady=5)

        # Center widgets
        tk.Grid.rowconfigure(self, 1)
        tk.Grid.columnconfigure(self, 0, weight=1)

    # Reset everything to default
    def refresh(self, controller):
        self.combobox_region.current(0)
        self.update_town_combobox(self.combobox_region.get())
        self.combobox_flat_types.current(0)
        self.update_table(self.results_frame)
        controller.show_frame(SelectOptions)

    # Setting values of town combobox according to region combobox
    def update_town_combobox(self, control):
        town_list = filter.dict_input('region', self.combobox_region.get())
        if town_list[0] != self.CONST_SELECT_TOWN:
            town_list = [self.CONST_SELECT_TOWN] + town_list
        self.combobox_town['values'] = town_list
        self.combobox_town.current(0)

    def town_selected(self, control):
        town_list = filter.dict_input('region', self.combobox_region.get())
        if town_list[0] != self.CONST_SELECT_TOWN:
            town_list = [self.CONST_SELECT_TOWN] + town_list
        self.combobox_town['values'] = town_list

    def update_table(self, frame):
        for child in frame.winfo_children():
            child.destroy()
        if not frame.winfo_ismapped():
            frame.grid(row=3)

        selected_region = self.combobox_region.get()
        selected_town = self.combobox_town.get()
        selected_flat_type = self.combobox_flat_types.get()
        if selected_region == self.CONST_SELECT_REGION and selected_town == self.CONST_SELECT_TOWN \
                and selected_flat_type == self.CONST_SELECT_FLAT_TYPE:
            frame.grid_forget()
        results_label = tk.Label(frame, text='Your Results', font=NORM_FONT)
        results_label.grid(row=1, columnspan=3)
        if selected_region != self.CONST_SELECT_REGION:
            # Return selected option for region
            region_label = tk.Label(frame, text='Region: ' + selected_region)
            region_label.grid(row=2, column=0)
        if selected_town != self.CONST_SELECT_TOWN:
            # Return selected option for town
            town_label = tk.Label(frame, text='Town: ' + selected_town)
            town_label.grid(row=2, column=1)
        if selected_flat_type != self.CONST_SELECT_FLAT_TYPE:
            # Return selected option for flat type
            flat_label = tk.Label(frame, text='Flat Type: ' + selected_flat_type)
            flat_label.grid(row=2, column=2)

        global filters
        # Get the filter options from combobox
        filters = {'region': selected_region, 'town': selected_town, 'flat_type': selected_flat_type}
        # Remove item from dict if default selection
        for item in list(filters):
            if filters[item] == self.CONST_SELECT_REGION or filters[item] == self.CONST_SELECT_TOWN \
                    or filters[item] == self.CONST_SELECT_FLAT_TYPE:
                del filters[item]

        # Update df according to updated filtered options
        filtered_data = filter.get_filtered_data(filters)
        rename_columns(filtered_data)
        # Return total number of records for search results
        total_records = str(len(filtered_data))
        total_rows_label = tk.Label(frame, text='Total number of records found: ' + total_records)
        total_rows_label.grid(row=3, columnspan=3)

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
        if total_records == '0':
            del filtered_data
            self.table_frame.grid_forget()
            self.export_button.grid_forget()
            self.is_table_deleted = True
            validation_label = tk.Label(frame,
                                        text='Sorry, no matching records found based on filters. Please '
                                             'try another search criterion.', font=VALIDAITON_FONT,
                                        fg='red')
            validation_label.grid(row=4, columnspan=3)

    # Top 10 Window
    def show_top10(self):
        for item in list(filters):
            if filters[item] == self.CONST_SELECT_REGION or filters[item] == self.CONST_SELECT_TOWN \
                    or filters[item] == self.CONST_SELECT_FLAT_TYPE:
                del filters[item]
        mainApp = ViewTop10CheapestFlatsWindow()
        mainApp.title('Top 10 Cheapest Flats')
        mainApp.geometry('1300x600')
        mainApp.mainloop()

    # Export Window
    @staticmethod
    def export_csv():
        file = asksaveasfile(filetypes=[('CSV Files', '*.csv')], defaultextension=[('CSV Files', '*.csv')],
                             initialfile='ResaleFlatPrices.csv')
        if file is not None:
            export.export_to_csv(file.name, filters)


class AverageByFlatType(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = None
        self.toolbar = None
        label = tk.Label(self, text='Analyse Resale Flats by Town', font=HEADER_FONT)
        label.pack(padx=0, pady=30)

        back_button = tk.Button(self, text='Back to Home', font=BUTTON_FONT, background='#007C89',
                                foreground="white", cursor='hand2',
                                command=lambda: self.refresh(controller))
        back_button.pack()

        # Add dropdown list with list of towns:
        town_list_options = dh.get_all_towns()
        clicked = tk.StringVar()
        clicked.set(town_list_options[0])

        # Add Combobox with the list of towns onto the GUI:
        self.town_combobox = ttk.Combobox(self, value=['Select Town'] + town_list_options, state='readonly',
                                          background="#007C89")
        self.town_combobox.current(0)
        self.town_combobox.bind('<<ComboboxSelected>>', self.selected)
        self.town_combobox.pack(pady=10)

        # Initialise default bar graph
        self.selected('')

    # Run this function when user selects from the dropdown list
    def selected(self, event):
        """This function is run when the user selects from the dropdown list. It removes the current graph and toolbar and adds the updated bar graph and dipslays the toolbar onto the ViewCharts window.
        Parameter: the event from the combobox"""

        # Clear the previous chart & toolbar first if it is currently on the screen
        try:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
        except AttributeError:
            pass

        # Add the bar graph into the ViewCharts window
        self.canvas = FigureCanvasTkAgg(bg.plot_bargraph(self.town_combobox.get()), master=self)
        # to display toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def refresh(self, controller):
        """This function is run when the user selects the 'Back to Home' button. It refreshes the dropdown list value
        back to the default and displays 'Select Town' on the dropdown list. Then, it displays the SelectOptions
        page. """
        self.town_combobox.current(0)
        self.selected('')
        controller.show_frame(SelectOptions)


class AverageByRegion(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.focus_set()
        self.bind('<Configure>', self.on_configure)

        top_frame = tk.Frame(self)
        top_frame.grid(row=0)
        label = tk.Label(top_frame, text='Analyse Resale Flats by Region', font=HEADER_FONT)
        label.pack(pady=10)

        back_button = tk.Button(top_frame, text='Back to Home', font=BUTTON_FONT, background='#007C89',
                                foreground="white", cursor='hand2',
                                command=lambda: controller.show_frame(SelectOptions))
        back_button.pack(pady=20)

        # Browser
        self.browser_frame = EmbeddedBrowser(self, controller)
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


class EmbeddedBrowser(tk.Frame):
    def __init__(self, parent, controller):
        self.browser = None
        tk.Frame.__init__(self, parent)
        self.bind('<FocusIn>', self.on_focus_in)
        self.bind('<FocusOut>', self.on_focus_out)
        self.bind('<Configure>', self.on_configure)
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        v = tk.StringVar()
        v.set('https://chart-studio.plotly.com/~si00/1.embed')
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info, url='https://chart-studio.plotly.com/~si00/1.embed',
                                             window_title='Tree Map')
        assert self.browser
        self.browser.SetClientHandler(LoadHandler(self))
        self.message_loop_work()

    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception('Couldn\'t obtain window handle')

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


if __name__ == '__main__':
    app = WelcomeWindow()
    app.title('HDB Resale Flats Analyser')
    width, height = app.winfo_screenwidth(), app.winfo_screenheight()  # Retrieve screen size
    app.geometry('%dx%d' % (width, height))  # Set full screen with tool bar on top
    cef.Initialize()
    app.mainloop()
    cef.Shutdown()
