import tkinter as tk
from tkinter import ttk
import bargraph
import data_helper
# from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


LARGE_FONT = ("Open Sans", 30)
NORM_FONT = ("Open Sans", 20)
SMALL_FONT = ("Open Sans", 15)

if __name__ == "__main__":

    class WelcomeWindow(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            container = tk.Frame(self)
            container.pack(side="top", fill="both", expand=True) #fill will fill in the space that the pack has been allotted to. expand will fill up the rest of the white space
            container.grid_rowconfigure(0, weight=1) #0 is the minimum size, weight is priority
            container.grid_columnconfigure(0, weight=1)
            self.frames = {}

            # all pages must be included in this dictionary in order to be raised to the top (accessed)
            for F in (SelectOptions, ViewCharts, ViewSummary):
                frame = F(container, self)

                self.frames[F] = frame

                # put all of the pages in the same location;
                # the one on the top of the stacking order
                # will be the one that is visible.
                frame.grid(row=0, column=0, sticky="nsew") #sticky will stretch everything to the size of the window
            self.show_frame(SelectOptions)

        def show_frame(self, cont):
            # show a frame for the given page name
            frame = self.frames[cont] #looks for the value in self.frames with this key
            frame.tkraise() #raises the frame to the front


    class SelectOptions(tk.Frame):
        def __init__(self, parent, controller):
            #self --> current object
            #parent --> a widget to act as the parent of the current object. All widgets in tkinter except the root window require a parent (sometimes also called a master)
            #controller -->some other object that is designed to act as a common point of interaction for several pages of widgets

            tk.Frame.__init__(self, parent) #parent --> parent class (WelcomeWindow)
            self.createLabels()
            self.createButtons(controller)

        def createLabels(self):
            header = tk.Label(self,text="HDB Resale Flats Analyser", font=LARGE_FONT) #created the header object
            label = tk.Label(self,
                text="This service enables you to check the resale flat prices within the last 3 years based on regions, "
                     "towns and flat-types.",
                font=SMALL_FONT, wraplength=450)
            header.pack(padx=0, pady=20) #pack is to place it on the page. padx or pady -> horizontal/vertical internal padding.
            label.pack(padx=10, pady=10)

        def createButtons(self, controller):
            #lambda creates a throwaway function that will only be here when it is called.
            #it cannot be used to pass parameters through
            # shows the ViewCharts class page upon clicking the button
            chartsBTN = tk.Button(self, text="View Charts", height=5, width=30, font=SMALL_FONT,
                                  command=lambda: controller.show_frame(ViewCharts))
            chartsBTN.pack(pady=10, padx=10)

            # shows the ViewSummary class page upon clicking the button
            summaryBTN = tk.Button(self, text="View Summary", height=5, width=30, font=SMALL_FONT,
                                   command=lambda: controller.show_frame(ViewSummary))
            summaryBTN.pack()

    # Setting up the ViewCharts page
    class ViewCharts(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="Analyse Resale Flats by Region", font=NORM_FONT)
            label.pack(padx=10, pady=10)

            # Run this function when user selects from the dropdown list
            def selected(event):
                # Clear the previous chart first if it is currently on the screen
                try:
                    self.canvas.get_tk_widget().pack_forget()
                except AttributeError:
                    pass

                # Add the graph from bargraph.py into the ViewCharts window
                self.canvas = FigureCanvasTkAgg(bargraph.plot_bar_graph(self.town_combobox.get()), master=self)
                self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

            #Add dropdown list with list of towns:
            town_list_options = data_helper.get_all_towns()
            # town_list_options.insert(0, "SINGAPORE")
            clicked = tk.StringVar()
            clicked.set(town_list_options[0])

            #Option Menu - not using
            # town_menu = tk.OptionMenu(self, clicked, *town_list_options, command=selected)
            # town_menu.pack(pady=20)

            #Add Combobox with the list of towns onto the GUI:
            self.town_combobox = ttk.Combobox(self, value=town_list_options)
            self.town_combobox.current(0)
            self.town_combobox.bind("<<ComboboxSelected>>", selected)
            self.town_combobox.pack()

            backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
            backbutton.pack(padx=10, pady=10)

    # Setting up the ViewSummary page
    class ViewSummary(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="Resale Flats Summary", font=NORM_FONT)
            label.pack(pady=10, padx=10)

            backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
            backbutton.pack()


    app = WelcomeWindow()
    app.title("HDB Resale Flats Analyser") #sets title of window
    app.geometry("1920x1080") #sets dimensions of tkinter window
    app.mainloop() #infinite loop so that events get processed
