import tkinter as tk
from tkinter import ttk
# import bargraph
from bargraph import get_filtered_data
import data_helper
# from matplotlib.figure import Figure
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter.tix import *
# from tkinterhtml import HtmlFrame
# import urllib.request
from cefpython3 import cefpython as cef
import sys
from numpy import arange
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
import platform
import ctypes

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

LARGE_FONT = ("Open Sans", 30)
NORM_FONT = ("Open Sans", 20)
SMALL_FONT = ("Open Sans", 15)
CONST_FILE_PATH = "resources/bargraph.png"

if __name__ == "__main__":

    class WelcomeWindow(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)
            container.pack(side="top", fill="both",
                           expand=True)  # fill will fill in the space that the pack has been allotted to. expand will fill up the rest of the white space
            container.grid_rowconfigure(0, weight=1)  # 0 is the minimum size, weight is priority
            container.grid_columnconfigure(0, weight=1)
            self.frames = {}

            # all pages must be included in this dictionary in order to be raised to the top (accessed)
            for F in (SelectOptions, ViewCharts, MainBrowser, ViewSummary):
                frame = F(container, self)

                self.frames[F] = frame

                # put all of the pages in the same location;
                # the one on the top of the stacking order
                # will be the one that is visible.
                frame.grid(row=0, column=0, sticky="nsew")  # sticky will stretch everything to the size of the window
            self.show_frame(SelectOptions)

        def show_frame(self, cont):
            # show a frame for the given page name
            frame = self.frames[cont]  # looks for the value in self.frames with this key
            frame.tkraise()  # raises the frame to the front


    class SelectOptions(tk.Frame):
        def __init__(self, parent, controller):
            # self --> current object
            # parent --> a widget to act as the parent of the current object. All widgets in tkinter except the root window require a parent (sometimes also called a master)
            # controller -->some other object that is designed to act as a common point of interaction for several pages of widgets

            tk.Frame.__init__(self, parent)  # parent --> parent class (WelcomeWindow)
            self.createLabels()
            self.createButtons(controller)

        def createLabels(self):
            header = tk.Label(self, text="HDB Resale Flats Analyser", font=LARGE_FONT)  # created the header object
            label = tk.Label(self,
                             text="This service enables you to check the resale flat prices within the last 3 years based on regions, "
                                  "towns and flat-types.",
                             font=SMALL_FONT, wraplength=450)
            header.pack(padx=0,
                        pady=20)  # pack is to place it on the page. padx or pady -> horizontal/vertical internal padding.
            label.pack(padx=10, pady=10)

        def createButtons(self, controller):
            # lambda creates a throwaway function that will only be here when it is called.
            # it cannot be used to pass parameters through
            # shows the ViewCharts class page upon clicking the button
            chartsBTN = tk.Button(self, text="View Charts", height=5, width=30, font=SMALL_FONT,
                                  command=lambda: controller.show_frame(ViewCharts))
            chartsBTN.pack(pady=10, padx=10)

            treemapBTN = tk.Button(self, text="View Tree Map", height=5, width=30, font=SMALL_FONT,
                                   command=lambda: controller.show_frame(MainBrowser))
            treemapBTN.pack(pady=10, padx=10)

            # shows the ViewSummary class page upon clicking the button
            summaryBTN = tk.Button(self, text="View Summary", height=5, width=30, font=SMALL_FONT,
                                   command=lambda: controller.show_frame(ViewSummary))
            summaryBTN.pack()


    # Setting up the ViewCharts page
    class ViewCharts(tk.Frame):

        def plot_bar_graph(self, town='', year=''):
            try:
                town = town.upper()
                year = int(year) if year != '' else year
                df = get_filtered_data(town, year)
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
                print('Year is not an integer!')
            except IndexError:
                print('No data found!')

        # Run this function when user selects from the dropdown list
        def selected(self, event):
            # Clear the previous chart & toolbar first if it is currently on the screen
            try:
                self.canvas.get_tk_widget().pack_forget()
                self.toolbar.pack_forget()
            except AttributeError:
                pass

            # Add the graph from bargraph.py into the ViewCharts window
            self.canvas = FigureCanvasTkAgg(self.plot_bar_graph(self.town_combobox.get()), master=self)

            # to display toolbar
            self.toolbar = NavigationToolbar2Tk(self.canvas, self)
            self.toolbar.update()

            self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # def onFrameConfigure(self, event):
        #     '''Reset the scroll region to encompass the inner frame'''
        #     self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)

            # for scrollbar - wrong
            # self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
            # self.frame = tk.Frame(self.canvas, background="#ffffff")
            # self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
            # self.canvas.configure(yscrollcommand=self.vsb.set)
            #
            # self.vsb.pack(side="right", fill="y")
            # self.canvas.pack(side="left", fill="both", expand=True)
            # self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
            #                           tags="self.frame")
            #
            # self.frame.bind("<Configure>", self.onFrameConfigure)

            label = tk.Label(self, text="Analyse Resale Flats by Region", font=NORM_FONT)
            label.pack(padx=10, pady=10)

            # Add dropdown list with list of towns:
            town_list_options = data_helper.get_all_towns()
            # town_list_options.insert(0, "SINGAPORE")
            clicked = tk.StringVar()
            clicked.set(town_list_options[0])

            # Option Menu - not using
            # town_menu = tk.OptionMenu(self, clicked, *town_list_options, command=selected)
            # town_menu.pack(pady=20)

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


    # Setting up the ViewSummary page
    class ViewSummary(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="Resale Flats Summary", font=NORM_FONT)
            label.pack(pady=10, padx=10)

            backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
            backbutton.pack()


    app = WelcomeWindow()
    app.title("HDB Resale Flats Analyser")  # sets title of window
    app.geometry("1920x1080")  # sets dimensions of tkinter window
    cef.Initialize()
    app.mainloop()  # infinite loop so that events get processed
    cef.Shutdown()
