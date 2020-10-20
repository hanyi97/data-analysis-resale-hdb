from tksheet import Sheet
import tkinter as tk
import pandas as pd
import data_helper

class demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        df = data_helper.get_dataframe()
        testdata = df.values.tolist()
        testdata = sorted(testdata, key=lambda x: x[0]) # Sort by ascending year
        testdata = sorted(testdata, key=lambda x: x[1]) # Sort by ascending month
        head = df.columns
        headerList = head.values.tolist()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.sheet = Sheet(self.frame,
                           page_up_down_select_row=True,
                           # empty_vertical = 0,
                           column_width=95,
                           startup_select=(0, 1, "rows"),
                           data=testdata, #to set sheet data at startup
                           headers = headerList,
                           # row_index = [f"Row {r}\nnewline1\nnewline2" for r in range(2000)],
                           # set_all_heights_and_widths = True, #to fit all cell sizes to text at start up
                           # headers = 0, #to set headers as first row at startup
                           # theme = "blue",
                           # row_index = 0, #to set row_index as first column at startup
                           height=500,  # height and width arguments are optional
                           width=1000  # For full startup arguments see DOCUMENTATION.md
                           )

        self.sheet.enable_bindings(("single_select",  # "single_select" or "toggle_select"
                                    "drag_select",  # enables shift click selection as well
                                    "column_drag_and_drop",
                                    "row_drag_and_drop",
                                    "column_select",
                                    "row_select",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    # "row_width_resize",
                                    # "column_height_resize",
                                    "arrowkeys",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "hide_columns",
                                    "copy",
                                    "undo"
                                    ))

        self.frame.grid(row=0, column=0, sticky="nswe")
        self.sheet.grid(row=0, column=0, sticky="nswe")

        # __________ DISPLAY SUBSET OF COLUMNS __________
        indexList = []
        for i in range(len(df.columns)):
            indexList.append(i)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.sheet.display_subset_of_columns(indexes=indexList, enable=True)
        # self.sheet.display_columns(enable = False)
        self.sheet.insert_columns(columns=0, idx=len(testdata), mod_column_positions=False)


        """_________________________ EXAMPLES _________________________ """
        """_____________________________________________________________"""

        # __________ CHANGING THEME __________

        # self.sheet.change_theme("light green")



        # __________ CELL / ROW / COLUMN ALIGNMENTS __________

        #self.sheet.align_cells(row=1, column=1, align="e")
        # self.sheet.align_rows(rows=3, align="e")
        # self.sheet.align_columns(columns=4, align="e")

        # __________ BINDING A FUNCTIONS TO USER ACTIONS __________

        # self.sheet.extra_bindings([("cell_select", self.cell_select),
        #                            ("begin_edit_cell", self.begin_edit_cell),
        #                           ("end_edit_cell", self.end_edit_cell),
        #                            ("shift_cell_select", self.shift_select_cells),
        #                            ("drag_select_cells", self.drag_select_cells),
        #                            ("ctrl_a", self.ctrl_a),
        #                            ("row_select", self.row_select),
        #                            ("shift_row_select", self.shift_select_rows),
        #                            ("drag_select_rows", self.drag_select_rows),
        #                            ("column_select", self.column_select)
        #                            ("shift_column_select", self.shift_select_columns),
        #                            ("drag_select_columns", self.drag_select_columns),
        #                            ("deselect", self.deselect)
        #                            ])
        # self.sheet.extra_bindings("bind_all", self.all_extra_bindings)
        # self.sheet.extra_bindings("begin_edit_cell", self.begin_edit_cell)
        # self.sheet.extra_bindings([("cell_select", None)]) #unbind cell select
        # self.sheet.extra_bindings("unbind_all") #remove all functions set by extra_bindings()

        # __________ BINDING NEW RIGHT CLICK FUNCTION __________

        # self.sheet.bind("<3>", self.rc)

        # __________ SETTING HEADERS __________

        # self.sheet.headers((f"Header {c}" for c in range(30))) #any iterable works
        # self.sheet.headers("Change header example", 2)
        # print (self.sheet.headers())
        # print (self.sheet.headers(index = 2))

        # __________ SETTING ROW INDEX __________

        # self.sheet.row_index((f"Row {r}" for r in range(2000))) #any iterable works
        # self.sheet.row_index("Change index example", 2)
        # print (self.sheet.row_index())
        # print (self.sheet.row_index(index = 2))

        # __________ INSERTING A ROW __________

        # self.sheet.insert_row(values = (f"my new row here {c}" for c in range(30)), idx = 0) # a filled row at the start
        # self.sheet.insert_row() # an empty row at the end

        # __________ INSERTING A COLUMN __________

        # self.sheet.insert_column(values = (f"my new col here {r}" for r in range(2050)), idx = 0) # a filled column at the start
        # self.sheet.insert_column() # an empty column at the end

        # __________ SETTING A COLUMNS DATA __________

        # any iterable works
        # self.sheet.set_column_data(0, values = (0 for i in range(2050)))

        # __________ SETTING A ROWS DATA __________

        # any iterable works
        # self.sheet.set_row_data(0, values = (0 for i in range(35)))

        # __________ SETTING A CELLS DATA __________

        # self.sheet.set_cell_data(1, 2, "NEW VALUE")

        # __________ GETTING FULL SHEET DATA __________

        # self.all_data = self.sheet.get_sheet_data()

        # __________ GETTING CELL DATA __________

        # print (self.sheet.get_cell_data(0, 0))

        # __________ GETTING ROW DATA __________

        # print (self.sheet.get_row_data(0)) # only accessible by index

        # __________ GETTING COLUMN DATA __________

        # print (self.sheet.get_column_data(0)) # only accessible by index

        # __________ GETTING SELECTED __________

        # print (self.sheet.get_currently_selected())
        # print (self.sheet.get_selected_cells())
        # print (self.sheet.get_selected_rows())
        # print (self.sheet.get_selected_columns())
        # print (self.sheet.get_selection_boxes())
        # print (self.sheet.get_selection_boxes_with_types())

        # __________ SETTING SELECTED __________

        # self.sheet.deselect("all")
        # self.sheet.create_selection_box(0, 0, 2, 2, type_ = "cells") #type here is "cells", "cols" or "rows"
        # self.sheet.set_currently_selected(0, 0)
        # self.sheet.set_currently_selected("row", 0)
        # self.sheet.set_currently_selected("column", 0)

        # __________ CHECKING SELECTED __________

        # print (self.sheet.cell_selected(0, 0))
        # print (self.sheet.row_selected(0))
        # print (self.sheet.column_selected(0))
        # print (self.sheet.anything_selected())
        # print (self.sheet.all_selected())

        # __________ HIDING THE ROW INDEX AND HEADERS __________

        # self.sheet.hide("row_index")
        # self.sheet.hide("top_left")
        # self.sheet.hide("header")

        # __________ ADDITIONAL BINDINGS __________

        # self.sheet.bind("<Motion>", self.mouse_motion)

    """

    UNTIL DOCUMENTATION IS COMPLETE, PLEASE BROWSE THE FILE
    _tksheet.py FOR A FULL LIST OF FUNCTIONS AND THEIR PARAMETERS

    """

    # def all_extra_bindings(self, event):
    #     print(event)

    # def begin_edit_cell(self, event):
    #     print(event)  # event[2] is keystroke
    #     return event[2]  # return value is the text to be put into cell edit window
    #
    # def end_edit_cell(self, event):
    #     print(event)

    # def window_resized(self, event):
    #     pass
    #     # print (event)

app = demo()
app.mainloop()