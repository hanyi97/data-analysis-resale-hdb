import tkinter as tk
from tkinter import ttk


class WelcomeWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = displaySummary(self)
        t.pack(side="top", fill="x")


class displaySummary(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)

        filterOptions=["Year","Month","Town","Flat Type","Flat Model","Lease Commence Date","Remaining Lease","Resale Price","Region"]

        # combobox
        self.comboBoxOrderGroup = ttk.Combobox(self, state="readonly")
        self.comboBoxOrderGroup.pack(pady=0, padx=0)
        # self.comboBoxOrderGroup.bind('<<ComboboxSelected>>',
        #                              lambda x: self.updateGraphNic(self.comboBoxOrderGroup.get()))
        self.comboBoxOrderGroup['values'] = filterOptions
        self.comboBoxOrderGroup.current(0)

    # def __init__(self, parent, rows=10, columns=9):
    #     tk.Frame.__init__(self, parent, background="black")
    #     self._widgets = []
    #     for row in range(rows):
    #         current_row = []
    #         for column in range(columns):
    #             label = tk.Label(self, text="%s/%s" % (row, column),
    #                              borderwidth=0, width=10)
    #             label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
    #             current_row.append(label)
    #         self._widgets.append(current_row)
    #
    #     for column in range(columns):
    #         self.grid_columnconfigure(column, weight=1)
    #
    #
    # def set(self, row, column, value):
    #     widget = self._widgets[row][column]
    #     widget.configure(text=value)


app = WelcomeWindow()
app.title("HDB Resale Flats Analyser")
app.geometry("600x600")
app.mainloop()
