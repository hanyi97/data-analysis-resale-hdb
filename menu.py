import tkinter as tk

LARGE_FONT = ("Open Sans", 30)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


class WelcomeWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = WelcomePage(container, self)
        self.frames[WelcomePage] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(WelcomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.createLabels()
        self.createButtons(controller)

    def createLabels(self):
        label = tk.Label(text="HDB Resale Flats Analyzer", font=LARGE_FONT)
        label.pack(pady=0, padx=10)

    def createButtons(self, controller):
        chartsBTN = tk.Button(self, text="View Charts", height=5, width=30)
        chartsBTN.pack(pady=0, padx=10)
        summaryBTN = tk.Button(self, text="View Summary",height=5, width=30)
        summaryBTN.pack(pady=0, padx=10)


app = WelcomeWindow()
app.title("ICT1002 Project")
app.geometry("500x600")
app.mainloop()
