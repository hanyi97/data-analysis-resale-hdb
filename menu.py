import tkinter as tk

LARGE_FONT = ("Open Sans", 30)
NORM_FONT = ("Open Sans", 20)
SMALL_FONT = ("Open Sans", 15)


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
        header = tk.Label(self,text="HDB Resale Flats Analyser", font=LARGE_FONT)
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


class ViewCharts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Analyse Resale Flats by Region", font=NORM_FONT)
        label.pack(padx=10, pady=10)

        backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack(padx=10, pady=10)


class ViewSummary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Resale Flats Summary", font=NORM_FONT)
        label.pack(pady=10, padx=10)

        backbutton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(SelectOptions))
        backbutton.pack()


app = WelcomeWindow()
app.title("HDB Resale Flats Analyser")
app.geometry("600x600")
app.mainloop()
