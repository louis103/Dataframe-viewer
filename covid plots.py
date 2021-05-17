from tkinter import messagebox
from tkinter import scrolledtext
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import lxml, requests
from tkinter import *
from tkinter import ttk, filedialog
import time, datetime
import urllib,urllib3
from urllib.request import urlopen
import json

class Tkinter_dataframe_viewer:

    def __init__(self, master):
        super(Tkinter_dataframe_viewer, self).__init__()
        self.root = master
        self.root.iconbitmap('pd-icon.ico')
        self.root.geometry('1350x700')
        with open('settings.json') as d:
            j = json.load(d)
            bg = j['bg']
        # self.root.configure(bg=bg)
        self.root.tk_setPalette(background=bg)
        self.style = ttk.Style()
        plt.style.use('fivethirtyeight')
        self.style.theme_use('clam')
        self.style.configure('Treeview.Heading', foreground="red", font=('Courier', 13, 'bold'))
        self.style.configure('.', font=('Courier', 12), background='white')
        self.style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=20,
            fieldbackground="white"
        )
        self.style.map('Treeview', background=[('selected', 'lightblue')])
        self.root.title('data analysis window')

        self.my_menu = Menu(self.root)
        self.root.configure(menu=self.my_menu)
        self.clear = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="File", menu=self.clear)
        self.clear.add_command(label="Open Excel file now", command=self.open_excel)
        self.clear.add_command(label="Open Csv file now", command=self.open_csv)
        self.clear.add_command(label="Convert table to CSV Format", command=self.to_csv_file)
        self.clear.add_command(label="Convert table to EXCEL Format", command=self.to_excel_file)
        self.clear.add_command(label="Exit now", command=self.root.quit)
        self.setting = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Settings", menu=self.setting)
        self.setting.add_command(label="Review settings",command=self.get_Settings)
        self.gps_ = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Documentation panel", menu=self.gps_)
        self.gps_.add_command(label="View Documentation", command=self.gps_ext)
        self.covid_ = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Covid 19 Updates", menu=self.covid_)
        self.covid_.add_command(label="View Updates",font=('Verdana',13),command=self.validate)
        self.covid_1 = Menu(self.my_menu, tearoff=False)
        self.my_menu.add_cascade(label="Covid 19 Data Table", menu=self.covid_1)
        self.covid_1.add_command(label="View Table", font=('Verdana', 13), command=self.validate_table)
        # self.dev = Menu(self.my_menu, tearoff=False)
        # self.my_menu.add_cascade(label="Chat Developer", menu=self.dev)
        # self.dev.add_command(label="Open chat box", command=self.chatty)

        self.browse_btn = Button(self.root, text="Browse Excel", font=('Arial', 12), relief=SOLID, bg="grey",
                                 fg="white", command=self.open_excel)
        self.browse_btn.place(x=30, y=5)
        self.browse_btn2 = Button(self.root, text="Browse Csv", font=('Arial', 12), relief=SOLID, bg="grey", fg="white",
                                  command=self.open_csv)
        self.browse_btn2.place(x=170, y=5)
        self.leb = Label(self.root, text="Simple mathematical computations \nfrom the columns(on your left)",
                         font=('Poppins', 13, 'italic'),fg="blue").place(x=290, y=4)
        self.max_value = Label(self.root, text="Max value: ", font=('Courier', 14, 'bold'))
        self.max_value.place(x=290, y=51)
        self.max_value_ans = Label(self.root, text="0", font=('Courier', 14, 'italic'))
        self.max_value_ans.place(x=460, y=51)
        self.mode = Label(self.root, text="NaN Count: ", font=('Courier', 14, 'bold'))
        self.mode.place(x=290, y=75)
        self.mode_ans = Label(self.root, text="0 ", font=('Courier', 14, 'italic'))
        self.mode_ans.place(x=460, y=75)

        self.min_value = Label(self.root, text="Min value: ", font=('Courier', 14, 'bold'))
        self.min_value.place(x=290, y=105)
        self.min_value_ans = Label(self.root, text="0.0", font=('Courier', 14, 'italic'))
        self.min_value_ans.place(x=460, y=105)

        self.valcount_value = Label(self.root, text="Value counts: ", font=('Courier', 14, 'bold'))
        self.valcount_value.place(x=290, y=138)
        self.valcount_value_ans = Label(self.root, text="0", font=('Courier', 14, 'italic'))
        self.valcount_value_ans.place(x=460, y=138)

        self.Mean_val = Label(self.root, text="Mean: ", font=('Courier', 14, 'bold'))
        self.Mean_val.place(x=290, y=165)
        self.mean_value_ans = Label(self.root, text="0.0", font=('Courier', 14, 'italic'))
        self.mean_value_ans.place(x=460, y=165)

        self.stdeviation_value = Label(self.root, text="Std: ", font=('Courier', 14, 'bold'))
        self.stdeviation_value.place(x=290, y=195)
        self.std_value_ans = Label(self.root, text="0.0", font=('Courier', 14, 'italic'))
        self.std_value_ans.place(x=460, y=195)

        self.total_sum_value = Label(self.root, text="Sum: ", font=('Courier', 14, 'bold'))
        self.total_sum_value.place(x=290, y=225)
        self.total_sum_value_ans = Label(self.root, text="0.0", font=('Courier', 14, 'italic'))
        self.total_sum_value_ans.place(x=460, y=225)
        self.median = Label(self.root, text="Median: ", font=('Courier', 14, 'bold'))
        self.median.place(x=290, y=247)
        self.median_ans = Label(self.root, text="0.0", font=('Courier', 14, 'italic'))
        self.median_ans.place(x=460, y=247)
        self.tot = Label(self.root, text="Total NaNs: ", font=('Courier', 14, 'bold'))
        self.tot.place(x=290, y=270)
        self.tot_ans = Label(self.root, text="0.0", font=('Courier', 14, 'italic'))
        self.tot_ans.place(x=460, y=270)

        self.l_frame1 = Frame(self.root, relief=SOLID)
        self.my_scrollbar = ttk.Scrollbar(self.l_frame1, orient=VERTICAL)
        self.listbox_columns = Listbox(self.l_frame1, width=20, height=11, yscrollcommand=self.my_scrollbar.set,
                                       font=('Courier', 14))

        self.listbox_columns.bind("<<ListboxSelect>>",self.get_selected)
        self.listbox_columns.pack()
        # self.calc = Button(self.root,text="Read JSON Data",relief=SOLID,font=('Poppins',14),width=17)
        # self.calc.place(x=60, y=260)
        # listbox_highest = Listbox(root,width=32,height=14)
        # listbox_highest.place(x=270,y=50)        # listbox_smallest = Listbox(root,width=29,height=14)
        # listbox_smallest.place(x=490,y=50)

        self.search = StringVar()
        self.search.set("Search values by...")
        self.options3 = ['Name', 'Age']
        self.cols_data = StringVar()
        # self.cols_data.set(self.options3[0])
        # listbox scrollbars
        self.my_scrollbar.config(command=self.listbox_columns.yview)
        #self.my_scrollbar.pack(side=RIGHT,fill=Y)
        self.l_frame1.place(x=30, y=50)

        # heading_label = Label(root,text="Your DataFrame in a Table format",font=('Arial',16,'bold'),fg="darkblue")
        # heading_label.place(x=890,y=5)
        self.search_label = Label(self.root, text="Search data below by the respective columns".upper(),
                                  font=('Times', 14, 'underline'), fg="blue")
        self.search_label.place(x=850, y=2)
        self.search_entry = Entry(self.root, width=25, font=('Courier', 14), relief=GROOVE,
                                  textvariable=self.search)
        self.search_entry.place(x=690, y=32)
        self.search_entry.bind("<KeyRelease>",self.search_Treeview_data)
        self.my_search_combo = ttk.Combobox(self.root, textvariable=self.cols_data, font=('Arial', 14), width=25)
        self.my_search_combo.place(x=990, y=32)
        self.plt_label = Label(self.root, text="Scatter plots", font=('Arial', 15, 'underline'), fg="green")
        self.plt_label.place(x=100, y=300)
        self.drop_label = Label(self.root, text="Drop Columns", font=('Arial', 14))
        self.drop_label.place(x=400, y=300)

        self.page_set = StringVar()
        self.drop = ttk.Combobox(self.root, textvariable=self.page_set, font=('Courier', 12))
        # no_of_pages.bind("<<ComboboxSelected>>", selected)
        self.drop.place(x=550, y=302)
        self.drop_btn = Button(self.root, text="Drop column", font=('Arial', 11), relief=SOLID, fg="black", width=14,
                               command=self.drop_columns)
        self.drop_btn.place(x=570, y=338)
        # SCATTER PLOTS
        self.scatter_frame = Frame(self.root, width=15, height=40, borderwidth=2, relief=SOLID)
        self.scatter_frame.place(x=30, y=330)
        self.v1 = StringVar()
        self.v2 = StringVar()
        self.v3 = StringVar()

        self.x = Label(self.scatter_frame, text="x-axis", font=('Courier', 12)).grid(row=0, column=0, padx=10, pady=10)
        self.x_entry = ttk.Combobox(self.scatter_frame, font=('Arial', 10), width=12, textvariable=self.v1)
        self.x_entry.grid(row=0, column=2, padx=10)
        self.y = Label(self.scatter_frame, text="y-axis", font=('Courier', 12)).grid(row=1, column=0, padx=10, pady=10)
        self.y_entry = ttk.Combobox(self.scatter_frame, font=('Arial', 10), width=12, textvariable=self.v2)
        self.y_entry.grid(row=1, column=2, padx=10)
        self.figx = Label(self.scatter_frame, text="Fig_size-x", font=('Courier', 12)).grid(row=3, column=0, padx=7,
                                                                                            pady=10)
        self.figx_e = Entry(self.scatter_frame, width=8, font=('Courier', 12))
        self.figx_e.grid(row=3, column=2)
        self.figy = Label(self.scatter_frame, text="Fig_size-y", font=('Courier', 12)).grid(row=4, column=0, padx=7,
                                                                                            pady=10)
        self.figy_e = Entry(self.scatter_frame, width=8, font=('Courier', 12))
        self.figy_e.grid(row=4, column=2)
        self.title_1 = Label(self.scatter_frame, text="Title", font=('Courier', 12)).grid(row=5, column=0, padx=7,
                                                                                          pady=10)
        self.title_1_entry = Entry(self.scatter_frame, width=12, font=('Courier', 12))
        self.title_1_entry.grid(row=5, column=2)
        self.show_btn = Button(self.root, text="Show Scatter Plot", font=('Courier', 14), relief=GROOVE, fg="black",
                               width=18, command=self.plot_scatter).place(x=42, y=580)

        self.plt_label = Label(self.root, text="Line plots", font=('Arial', 15, 'underline'), fg="orange")
        self.plt_label.place(x=340, y=325)
        self.a_label = Label(self.root, text="Active file name", font=('Poppins', 18), fg="blue")
        self.a_label.place(x=20, y=630)
        self.file_label = Label(self.root, text="C:/", font=('Courier', 17, 'underline'), fg="black")
        self.file_label.place(x=20, y=660)

        # LINE PLOTS
        self.v4 = StringVar()
        self.v5 = StringVar()
        self.v6 = StringVar()
        self.line_frame = Frame(self.root, width=20, height=40, borderwidth=2, relief=SOLID)
        self.line_frame.place(x=290, y=360)

        self.x1 = Label(self.line_frame, text="x-axis", font=('Courier', 12)).grid(row=0, column=0, pady=10)
        self.x_entry1 = ttk.Combobox(self.line_frame, font=('Arial', 10), width=12, textvariable=self.v4)
        self.x_entry1.grid(row=0, column=2, padx=10)
        self.y1 = Label(self.line_frame, text="y-axis", font=('Courier', 12)).grid(row=1, column=0, pady=10)
        self.y_entry2 = ttk.Combobox(self.line_frame, font=('Arial', 10), width=12, textvariable=self.v5)
        self.y_entry2.grid(row=1, column=2, padx=10)
        self.fig2x = Label(self.line_frame, text="Fig_size-x", font=('Courier', 12)).grid(row=3, column=0, pady=10)
        self.fig2x_e = Entry(self.line_frame, width=8, font=('Courier', 12))
        self.fig2x_e.grid(row=3, column=2)
        self.fig2y = Label(self.line_frame, text="Fig_size-y", font=('Courier', 12)).grid(row=4, column=0, pady=10)
        self.fig2y_e = Entry(self.line_frame, width=8, font=('Courier', 12))
        self.fig2y_e.grid(row=4, column=2)

        self.title_2 = Label(self.line_frame, text="Title", font=('Courier', 12)).grid(row=5, column=0, padx=7,
                                                                                       pady=10)
        self.title_2_entry = Entry(self.line_frame, width=12, font=('Courier', 12))
        self.title_2_entry.grid(row=5, column=2)

        self.show_line = Button(self.root, text="Show Line plot", font=('Courier', 14), relief=GROOVE, fg="black",
                                width=18, command=self.plot_line).place(x=310, y=600)

        self.plt_label2 = Label(self.root, text="Histogram plots", font=('Arial', 15, 'underline'), fg="red")
        self.plt_label2.place(x=565, y=370)

        # HISTOGRAM PLOTS
        self.v7 = StringVar()
        self.v8 = StringVar()
        self.v9 = StringVar()
        self.hist_frame = Frame(self.root, width=20, height=40, borderwidth=2, relief=SOLID)
        self.hist_frame.place(x=560, y=400)

        self.x3 = Label(self.hist_frame, text="x-axis", font=('Courier', 12)).grid(row=0, column=0, pady=10)
        self.x_entry4 = ttk.Combobox(self.hist_frame, font=('Arial', 10), width=12, textvariable=self.v7)
        self.x_entry4.grid(row=0, column=2, padx=10)
        # self.y4 = Label(self.hist_frame, text="y-axis", font=('Courier', 12)).grid(row=1, column=0, pady=10)
        # self.y_entry5 = ttk.Combobox(self.hist_frame, font=('Arial', 10), width=12, textvariable=self.v8)
        # self.y_entry5.grid(row=1, column=2, padx=10)
        self.figxbins = Label(self.hist_frame, text="No of Bins", font=('Courier', 12)).grid(row=3, column=0, pady=5)
        self.figxbins_e = Entry(self.hist_frame, width=8, font=('Courier', 12))
        self.figxbins_e.grid(row=3, column=2)
        self.fig3x = Label(self.hist_frame, text="Fig_size-x", font=('Courier', 12)).grid(row=4, column=0, pady=10)
        self.fig3x_e = Entry(self.hist_frame, width=8, font=('Arial', 12))
        self.fig3x_e.grid(row=4, column=2)
        self.fig3y = Label(self.hist_frame, text="Fig_size-y", font=('Courier', 12)).grid(row=5, column=0, pady=5)
        self.fig3y_e = Entry(self.hist_frame, width=8, font=('Courier', 12))
        self.fig3y_e.grid(row=5, column=2)

        self.title_3 = Label(self.hist_frame, text="Title", font=('Courier', 12)).grid(row=6, column=0,
                                                                                       pady=5)
        self.title_3_entry = Entry(self.hist_frame, width=12, font=('Courier', 12))
        self.title_3_entry.grid(row=6, column=2)

        self.show_hist = Button(self.root, text="Show Histogram", font=('Courier', 14), relief=SOLID,
                                fg="black",
                                width=15,command=self.plot_histogram).place(x=580, y=620)

        self.plt_label3 = Label(self.root, text="Bar plots", font=('Arial', 15, 'underline'), fg="blue")
        self.plt_label3.place(x=840, y=350)

        # BAR PLOTS
        self.v20 =StringVar()
        self.v21 = StringVar()
        self.heat_frame = Frame(self.root, width=20, height=40, borderwidth=2, relief=SOLID)
        self.heat_frame.place(x=810, y=390,width=250)
        self.b1 = Label(self.heat_frame, text="x-axis", font=('Courier', 12)).grid(row=0, column=0, pady=10)
        self.b2 = ttk.Combobox(self.heat_frame, font=('Arial', 10), width=12, textvariable=self.v20)
        self.b2.grid(row=0, column=1, padx=10)
        self.b3 = Label(self.heat_frame, text="y-axis", font=('Courier', 12)).grid(row=1, column=0, pady=10)
        self.b4 = ttk.Combobox(self.heat_frame, font=('Arial', 10), width=12, textvariable=self.v21)
        self.b4.grid(row=1, column=1, padx=10,pady=20)
        self.bt = Label(self.heat_frame, text="Title", font=('Courier', 12))
        self.bt.grid(row=2, column=0,pady=5)
        self.btentry = Entry(self.heat_frame, width=15, font=('Courier', 12))
        self.btentry.grid(row=2, column=1)
        self.show2 = Button(self.root, text="show barchart", font=('Arial', 12), relief=SOLID, bg="white",
                            fg="black",
                            width=15,command=self.plot_bar).place(x=850,y=550)

        self.pie = Label(self.root, text="View pie-chart Diagram", font=('Courier', 16, 'italic'), fg="red").place(
            x=1020, y=350)
        self.v30 = StringVar()
        self.v31 = StringVar()
        self.pie_frame = Frame(self.root, width=20, height=40, borderwidth=2, relief=SOLID)
        self.pie_frame.place(x=1080, y=390,width=240)
        self.b11 = Label(self.pie_frame, text="Values", font=('Courier', 12)).grid(row=0, column=0, pady=10)
        self.b22 = ttk.Combobox(self.pie_frame, font=('Arial', 10), width=12, textvariable=self.v30)
        self.b22.grid(row=0, column=1, padx=10)
        self.b33 = Label(self.pie_frame, text="Labels", font=('Courier', 12)).grid(row=1, column=0, pady=10)
        self.b44 = ttk.Combobox(self.pie_frame, font=('Arial', 10), width=12, textvariable=self.v31)
        self.b44.grid(row=1, column=1, padx=10, pady=20)
        self.bt = Label(self.pie_frame, text="Title", font=('Courier', 12))
        self.bt.grid(row=2, column=0, pady=5)
        self.btentry1 = Entry(self.pie_frame, width=15, font=('Courier', 12))
        self.btentry1.grid(row=2, column=1)
        self.show_pie = Button(self.root, text="Show Pie Chart", font=('Courier', 14), width=15, fg="black",
                               relief=SOLID,command=self.plot_pie).place(
            x=1100, y=550)

        self.small_text = scrolledtext.ScrolledText(self.root, width=50, height=6, font=('Poppins', 12),fg="purple")
        self.small_text.place(x=870, y=590)
        self.small_text.insert(1.0,
                               "*****This software has been\n created by programmer louis wambua.\nFor more info about softwares\nplease\n send your email to>>\n"
                               "wambualouis@gmail.com*****\n")

        self.drop_label2 = Label(self.root, text="Empty Columns", font=('Courier', 14))
        self.drop_label2.place(x=770, y=300)

        self.emp = StringVar()
        self.empty = ttk.Combobox(self.root, font=('Courier', 11),textvariable=self.emp)
        # no_of_pages.bind("<<ComboboxSelected>>", selected)
        self.empty.place(x=920, y=302)
        self.remove_nans = Button(self.root,relief=SOLID,bg="whitesmoke",fg="blue",text="Remove All NaN Rows",font=('Courier',12),width=20,command=self.remove_all_NaNs)
        self.remove_nans.place(x=1140,y=302)
        # treeview
        self.tree_frame = Frame(self.root, width=5, height=20)
        self.tree_frame.place(x=570, y=70, width=770)

        # self.cols = ["name", "Lastname", "grades", "profession", "phone no", "Id"]
        # self.tree = ttk.Treeview(self.tree_frame, height=9, show="headings", columns=self.cols)
        self.tree = ttk.Treeview(self.tree_frame, height=9)
        # self.tree.column('name', width=110, minwidth=20, anchor=CENTER)
        # self.tree.column('Lastname', width=110, minwidth=20, anchor=CENTER)
        # self.tree.column('grades', width=110, minwidth=20, anchor=CENTER)
        # self.tree.column('profession', width=110, minwidth=20, anchor=CENTER)
        # self.tree.column('phone no', width=110, minwidth=20, anchor=CENTER)
        # self.tree.column('Id', width=100, minwidth=20, anchor=CENTER)
        #
        # self.tree.heading('name', text="Name")
        # self.tree.heading('Lastname', text="Lastname")
        # self.tree.heading('grades', text="Grades")
        # self.tree.heading('profession', text="Profession")
        # self.tree.heading('phone no', text="Phone no.")
        # self.tree.heading('Id', text="Id")

        # y scroll
        self.yscroll = Scrollbar(self.tree_frame, orient=VERTICAL)
        self.yscroll.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=self.yscroll.set)
        self.yscroll.pack(fill=Y, side=RIGHT)
        # x scrollbar
        self.xscroll = Scrollbar(self.tree_frame, orient=HORIZONTAL)
        self.xscroll.config(command=self.tree.xview)
        self.tree.config(xscrollcommand=self.xscroll.set)
        self.xscroll.pack(fill=X, side=BOTTOM)

        # tree.pack(side=TOP,fill=BOTH,padx=25)
        # self.tree.pack()
    def search_Treeview_data(self,e):
        self.newdf = df
        self.newdf_cols = list(self.newdf.columns)
        self.serch_col = self.my_search_combo.get()
        self.value_serch = self.search_entry.get()
        self.serch_columns = self.obj_list
        index = self.newdf_cols.index(self.serch_col)
        self.newchild = self.tree.get_children()
        if self.value_serch.lower() == "":
            self.update_treeview(self.newdf)
        else:
            for item in self.newchild:
                if self.value_serch in self.tree.item(item)['values'][index].lower():
                    searched_result = self.tree.item(item)['values']
                    self.tree.delete(item)
                    self.tree.insert("", 0, values=searched_result)


    def open_excel(self):
        lab = Label(self.root, text="")
        lab.pack(pady=20)
        self.filename = filedialog.askopenfilename(
            initialdir="/Desktop/",
            title="Open excel File",
            filetype=(("Xlsx files", "*.xlsx"), ("All Files", "*.*"))  # *.xlsx Xlsx files
        )
        global df
        if self.filename:
            try:
                self.filename = r"{}".format(self.filename)
                df = pd.read_excel(self.filename)
                self.file_label.config(text=self.filename)
            except ValueError:
                messagebox.showwarning('VALUE ERROR', 'There was a value error in your file')
            except FileNotFoundError:
                messagebox.showwarning('FILE NOT FOUND ERROR', 'Your file was not found!')
        else:
            messagebox.showerror('FILE ERROR', 'You did not open a file!')
        self.clear_tree()
        self.check_empty_columns(df)
        # print(df)
        # self.get_treeview_columns()

        self.tree["column"] = list(df.columns)
        self.tree["show"] = "headings"
        for column in self.tree["column"]:
            self.tree.column(column, width=150, minwidth=95, anchor=W, stretch=YES)
            self.tree.heading(column, text=column, anchor=W)
        for col in list(df.columns):
            self.listbox_columns.insert(END, col)

        self.obj_cols = df.dtypes[df.dtypes == np.object_]
        self.obj_list = list(self.obj_cols.index)
        #['ESEQ/01655/2019', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7']

        # controlling comboboxes
        self.my_search_combo['values'] = self.obj_list
        self.my_search_combo.current(0)
        self.drop['values'] = list(df.columns)
        self.drop.current(0)
        self.x_entry['values'] = list(df.columns)
        self.x_entry.current(0)
        self.y_entry['values'] = list(df.columns)
        self.y_entry.current(0)
        self.x_entry1['values'] = list(df.columns)
        self.x_entry1.current(0)
        self.y_entry2['values'] = list(df.columns)
        self.y_entry2.current(0)
        self.x_entry4['values'] = list(df.columns)
        self.x_entry4.current(0)
        self.b2['values'] = list(df.columns)
        self.b2.current(0)
        self.b4['values'] = list(df.columns)
        self.b4.current(0)
        self.b22['values'] = list(df.columns)
        self.b22.current(0)
        self.b44['values'] = list(df.columns)
        self.b44.current(0)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.tree.insert("", "end", values=row)

        #        for item in df.columns:
        #     self.listbox_columns.insert(END, item)

        self.tree.pack()

    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.listbox_columns.delete(0, END)

    def open_csv(self):
        self.filename = filedialog.askopenfilename(
            initialdir="/Desktop/COVID-19-DATA/",  # C:\Users\LOUIS\Desktop\COVID-19-DATA
            title="Open CSV File",
            filetype=(("CSV files", "*.csv"), ("All Files", "*.*"))  # *.xlsx Xlsx files
        )
        global df
        if self.filename:
            try:
                self.filename = r"{}".format(self.filename)
                df = pd.read_csv(self.filename)
                self.file_label.config(text=self.filename)

            except ValueError:
                messagebox.showwarning('VALUE ERROR', 'There was a value error in your file')
            except FileNotFoundError:
                messagebox.showwarning('FILE NOT FOUND ERROR', 'Your file was not found!')
        else:
            messagebox.showerror('FILE ERROR', 'You did not open a file!')
        self.clear_tree()
        self.check_empty_columns(df)
        self.tree["column"] = list(df.columns)
        self.tree["show"] = "headings"
        for column in self.tree["column"]:
            self.tree.column(column, width=150, minwidth=95, anchor=W, stretch=YES)
            self.tree.heading(column, text=column, anchor=W)
        for col in list(df.columns):
            self.listbox_columns.insert(END, col)
        self.obj_cols = df.dtypes[df.dtypes == np.object_]
        self.obj_list = list(self.obj_cols.index)
        # controlling comboboxes
        self.my_search_combo['values'] = self.obj_list
        self.my_search_combo.current(0)
        self.drop['values'] = list(df.columns)
        self.drop.current(0)
        self.x_entry['values'] = list(df.columns)
        self.x_entry.current(0)
        self.y_entry['values'] = list(df.columns)
        self.y_entry.current(0)
        self.x_entry1['values'] = list(df.columns)
        self.x_entry1.current(0)
        self.y_entry2['values'] = list(df.columns)
        self.y_entry2.current(0)
        self.x_entry4['values'] = list(df.columns)
        self.x_entry4.current(0)
        self.b2['values'] = list(df.columns)
        self.b2.current(0)
        self.b4['values'] = list(df.columns)
        self.b4.current(0)
        self.b22['values'] = list(df.columns)
        self.b22.current(0)
        self.b44['values'] = list(df.columns)
        self.b44.current(0)
        # self.drp['values'] = list(df.columns)
        # self.drp.current(0)
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.tree.insert("", "end", values=row)

        # self.yscroll = ttk.Scrollbar(self.tree_frame, orient=VERTICAL)
        # self.yscroll.config(command=self.tree.yview)
        # self.tree.config(yscrollcommand=self.yscroll.set)
        # self.yscroll.pack(fill=Y, side=RIGHT)
        # # x scrollbar
        # self.xscroll = ttk.Scrollbar(self.tree_frame, orient=HORIZONTAL)
        # self.xscroll.config(command=self.tree.xview)
        # self.tree.config(xscrollcommand=self.xscroll.set)
        # self.xscroll.pack(fill=X, side=BOTTOM)

        self.tree.pack()

    def get_treeview_columns(self):
        global columns
        columns = list(df.columns)
        print(columns)

    def drop_columns(self):
        self.column_to_drop = self.drop.get()
        df.drop([self.column_to_drop], axis=1, inplace=True)
        # print('***dataframe after deletion***')
        # print(df)
        self.update_treeview(df)
    def to_csv_file(self):
        my_df = df
        filename = filedialog.asksaveasfilename(defaultextension='.csv',initialdir="C:/Desktop/",title="Save CSV file as",filetypes=(("csv files","*.csv"),))
        my_df.to_csv(filename,index=False,header=True,encoding='utf-8',na_rep='Unknown',float_format='%.2f')

    def to_excel_file(self):
        my_df = df
        filename = filedialog.asksaveasfilename(defaultextension='.xlsx',initialdir="C:/Desktop/",title="Save Excel file as",filetypes=(("Excel files","*.xlsx"),))
        my_df.to_excel(filename,index=False,header=True,encoding='utf-8',na_rep='Unknown',float_format='%.2f')

    def gps_ext(self):
        messagebox.showinfo('Documentation Info',
                      "Convert to excel will turn the table to excel format\n"
                      "Convert to csv will turn the table to csv format\n"
                      "drop columns btn will remove any column you want\n"
                      "Nan values are values that are null or empty\n"
                      "Below is a set of plotting sub windows to help you \n"
                      "visualize your data\n"
                      "you can search anything from the dataframe \nby the respective columns"
                      "file>exit will help you exit the app\n"
                      "bottom right contains info about developer!\n"
                      "after changing the background color,please reload for it\n"
                      "to edit changes.\n"
                      "Thank you and Welcome!!!")

    def update_treeview(self,dataframe):
        self.clear_tree()
        self.new_cols = dataframe.columns
        self.tree["column"] = list(self.new_cols)
        self.tree["show"] = "headings"
        for column in self.tree["column"]:
            self.tree.column(column, width=150, minwidth=95, anchor=W, stretch=YES)
            self.tree.heading(column, text=column, anchor=W)
        for col in list(self.new_cols):
            self.listbox_columns.insert(END, col)
        new_df_rows = dataframe.to_numpy().tolist()
        for row in new_df_rows:
            self.tree.insert("", "end", values=row)
        self.obj_cols = dataframe.dtypes[dataframe.dtypes == np.object_]
        self.obj_list = list(self.obj_cols.index)

        #updating the comboboxes as well
        self.my_search_combo['values'] = self.obj_list
        self.my_search_combo.current(0)
        self.drop['values'] = list(self.new_cols)
        self.drop.current(0)
        self.x_entry['values'] = list(self.new_cols)
        self.x_entry.current(0)
        self.y_entry['values'] = list(self.new_cols)
        self.y_entry.current(0)
        self.x_entry1['values'] = list(self.new_cols)
        self.x_entry1.current(0)
        self.y_entry2['values'] = list(self.new_cols)
        self.y_entry2.current(0)
        self.x_entry4['values'] = list(self.new_cols)
        self.x_entry4.current(0)
        self.b22['values'] = list(self.new_cols)
        self.b22.current(0)
        self.b44['values'] = list(self.new_cols)
        self.b44.current(0)
        self.b2['values'] = list(self.new_cols)
        self.b2.current(0)
        self.b4['values'] = list(self.new_cols)
        self.b4.current(0)

    def check_empty_columns(self,dataframe):
        self.empty_cols = dataframe.columns[dataframe.isna().any()].tolist()
        if self.empty_cols:
            self.empty['values'] = list(self.empty_cols)
            self.empty.current(0)
        else:
            self.emp.set('No columns with NaN Values')
            self.empty['values'] = ""

    def remove_all_NaNs(self):
        df.dropna(how='any',inplace=True)
        self.update_treeview(df)
        self.check_empty_columns(df)

    def get_selected(self,e):
        self.sel = self.listbox_columns.get(ANCHOR)
        self.math_df = df
        self.max_val = self.math_df[self.sel].max()
        self.max_value_ans.config(text=self.max_val)
        self.mode_val = self.math_df[self.sel].isna().sum()
        self.mode_ans.config(text=self.mode_val)
        self.min_val = self.math_df[self.sel][self.math_df[self.sel].idxmin()]
        self.min_value_ans.config(text=self.min_val)
        self.count = self.math_df[self.sel].count()
        self.valcount_value_ans.config(text=self.count)
        self.mean = self.math_df[self.sel].mean()
        self.mean_value_ans.config(text=self.mean)
        self.std = self.math_df[self.sel].std().round(2)
        self.std_value_ans.config(text=self.std)
        self.sum = self.math_df[self.sel].sum().round(2)
        self.total_sum_value_ans.config(text=self.sum)
        self.median_ = self.math_df[self.sel].median().round(2)
        self.median_ans.config(text=self.median_)

        self.tott = self.math_df.isna().sum().sum()
        self.tot_ans.config(text=self.tott)
    def plot_scatter(self):
        self.my_dataframe = df
        self.column_x = self.x_entry.get()
        self.column_y = self.y_entry.get()
        if self.column_x == "" and self.column_y == "":
            messagebox.showwarning('Blank inputs', 'Please fill the blank entries!!!')
        elif self.column_x == "" or self.column_y == "":
            messagebox.showwarning('Blank inputs', 'Please fill all blank entries!!!')
        self.newx = self.my_dataframe[self.column_x]
        self.newy = self.my_dataframe[self.column_y].astype(int)
        fx = self.figx_e.get()
        fy = self.figy_e.get()
        if fx == "":
            fx = 10
        if fy == "":
            fy = 6
        fig, ax = plt.subplots(1, figsize=(int(fx), int(fy)))
        fig.suptitle(str(self.title_1_entry.get()))
        ax.scatter(self.newx, self.newy, color="blue", alpha=0.9,linewidths=1,marker='o')
        plt.xticks(rotation=55)
        plt.ticklabel_format(useOffset=False,style='plain',axis='y')
        plt.tight_layout()
        plt.xlabel(self.x_entry.get())
        plt.ylabel(self.y_entry.get())
        plt.show()

    def plot_line(self):
        self.my_dataframe = df
        self.column_x = self.x_entry1.get()
        self.column_y = self.y_entry2.get()
        if self.column_x=="" and self.column_y=="":
            messagebox.showwarning('Blank inputs', 'Please fill the blank entries!!!')
        elif self.column_x=="" or self.column_y=="":
            messagebox.showwarning('Blank inputs', 'Please fill all blank entries!!!')
        self.newx = self.my_dataframe[self.column_x]
        self.newy = self.my_dataframe[self.column_y].astype(int)
        fx = self.fig2x_e.get()
        fy = self.fig2y_e.get()
        if fx=="":
            fx = 10
        if fy=="":
            fy=6
        fig, ax = plt.subplots(1, figsize=(int(fx), int(fy)))
        fig.suptitle(str(self.title_2_entry.get()))
        ax.plot(self.newx, self.newy, color="red")
        plt.yticks(fontsize=12)
        plt.xticks(rotation=55,fontsize=10)
        plt.ticklabel_format(useOffset=False, style='plain', axis='y')
        plt.tight_layout()
        plt.xlabel(self.x_entry1.get())
        plt.ylabel(self.y_entry2.get())
        plt.show()

    def plot_histogram(self):
        plt.style.use('fivethirtyeight')
        self.n_bins = self.figxbins_e.get()
        self.my_data = df
        self.x_1 = self.x_entry4.get()
        if self.n_bins=="" and self.x_1=="":
            messagebox.showwarning('Blank inputs','Please fill the blank entries!!!')
        elif self.n_bins=="" or self.x_1=="":
            messagebox.showwarning('Blank inputs', 'Please fill all blank entries!!!')
        self.col_to_plot = self.my_data[self.x_1]
        fx = self.fig3x_e.get()
        fy = self.fig3y_e.get()
        if fx == "":
            fx = 10
        if fy == "":
            fy = 6
        fig, ax = plt.subplots(1, figsize=(int(fx), int(fy)))
        fig.suptitle(str(self.title_3_entry.get()))
        plt.hist(self.col_to_plot,edgecolor='black')
        plt.xticks(rotation=55)
        plt.ticklabel_format(useOffset=False, style='plain', axis='y')
        plt.tight_layout()
        plt.show()

    def plot_bar(self):
        plt.style.use('ggplot')
        self.bar_df = df
        self.column_x = self.b2.get()
        self.column_y = self.b4.get()
        if self.column_x=="" and self.column_y=="":
            messagebox.showwarning('Blank inputs', 'Please fill the blank entries!!!')
        elif self.column_x=="" or self.column_y=="":
            messagebox.showwarning('Blank inputs', 'Please fill all blank entries!!!')
        self.newx = self.bar_df[self.column_x]
        self.newy = self.bar_df[self.column_y].astype(int)
        fig, ax = plt.subplots(1, figsize=(10,8))
        fig.suptitle(str(self.btentry.get()))
        plt.bar(self.newx,self.newy)
        plt.xticks(rotation=55)
        plt.ticklabel_format(useOffset=False, style='plain', axis='y')
        plt.xlabel(self.column_x)
        plt.ylabel(self.column_y)
        plt.tight_layout()
        plt.show()

        # self.data = list(self.my_data.columns)
        # self.plot_data = self.my_data[self.data].astype(int)
        # plt.imshow(self.plot_data,cmap='cool',interpolation='nearest')
        # plt.show()


    def plot_pie(self):
        v = self.b22.get()
        label = self.b44.get()
        if v=="" and label=="":
            messagebox.showwarning('Blank inputs','Please fill the blank entries!!!')
        elif v=="" or label=="":
            messagebox.showwarning('Blank inputs', 'Please fill all blank entries!!!')
        self.pi_df = df
        x = self.pi_df[v]
        labels = self.pi_df[label]

        plt.style.use('fivethirtyeight')
        # shadow=True

        plt.pie(x, labels=labels, wedgeprops={'edgecolor': 'blue'}, startangle=90,
                autopct='%1.1f%%')

        plt.title(self.btentry1.get().upper())
        plt.tight_layout()
        plt.show()

    def reset_all_widgets(self):
        self.listbox_columns.delete(0, END)
        self.max_value_ans.config(text="0.0")
        self.min_value_ans.config(text="0.0")
        self.valcount_value_ans.config(text="0.0")
        self.std_value_ans.config(text="0.0")
        self.total_sum_value_ans.config(text="0.0")
        self.mean_value_ans.config(text="0.0")

    def check_internet(self):
        try:
            urlopen('https://www.google.com', timeout=1)
            return True
        except urllib.error.URLError as err:
            print(err)
            return False
    def validate(self):
        if self.check_internet():
            self.open_labels()
           # t().open_covid19_data()
        else:
            self.popup_notify()
    def popup_notify(self):
        messagebox.showwarning('Internet Unavailability','Seems there is no Internet connection to View this data!')
    def validate_table(self):
        if self.check_internet():
            self.open_Table()
        else:
            self.popup_notify()
    def open_labels(self):
        root = Tk()
        root.title("Corona data Updates")
        root.geometry("1250x300")
        root.resizable(1,0)
        def fetch_covid_label_results():
            api = "https://disease.sh/v3/covid-19/all"
            json_data = requests.get(api).json()
            global total_cases_, \
                total_deaths, \
                total_recovered, \
                updated, \
                date
            total_cases_ = json_data['cases']
            total_deaths = json_data['deaths']
            total_recovered = json_data['recovered']
            updated = json_data['updated']
            date = datetime.datetime.fromtimestamp(updated / 1e3)

        fetch_covid_label_results()
        label1 = Label(root, text="Global Covid live updates", font=('Arial', 20, "bold"), fg="red").pack(pady=10)
        res_frame = LabelFrame(root, text="Results for Covid", borderwidth=5, labelanchor=N, relief=RIDGE,
                               font=('Arial', 17, 'bold'), fg="green")
        res_frame.pack(pady=2, padx=20, ipadx=10, expand=0)

        label_a = Label(res_frame, text="Total Global Corona cases", font=("Helvetica", 14, "underline"))
        label_a.grid(row=0, column=0, padx=30)

        total_cases = Label(res_frame, text=total_cases_, font=("Arial", 15, 'italic'), fg="INDIGO").grid(row=1,column=0,pady=10)
        death_cases = Label(res_frame, text=total_deaths, font=("Arial", 15, 'italic'), fg="#008000").grid(row=1,column=1,pady=10)
        rec_cases = Label(res_frame, text=total_recovered, font=("Arial", 15, 'italic'), fg="black").grid(row=1,column=2,pady=10)
        update = Label(res_frame, text=date, font=("Arial", 12, 'italic'), fg="black").grid(row=1, column=3, pady=10)
        label_b = Label(res_frame, text="Total Global Corona Death cases", font=("Helvetica", 14, "underline"))
        label_b.grid(row=0, column=1, padx=30)
        label_c = Label(res_frame, text="Total Global Corona Recovered cases", font=("Helvetica", 14, "underline"))
        label_c.grid(row=0, column=2, padx=30)
        label_d = Label(res_frame, text="Date updated: ", font=('Helvetica', 14, 'underline'))
        label_d.grid(row=0, column=3)
        root.mainloop()
    def open_Table(self):
        root = Tk()
        root.title("Corona data Table and treeview")
        root.geometry("1200x460")
        root.resizable(1,0)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('Treeview.Heading', foreground="red", font=('Courier', 13, 'bold'))
        style.configure('.', font=('Courier', 12), background='white')
        style.configure(
            "Treeview",
            background="grey",
            foreground="black",
            rowheight=35,
            fieldbackground="white"
        )
        style.map('Treeview', background=[('selected', 'magenta')])
        my_search_labelframe = LabelFrame(root, text="Search Table Data here!", borderwidth=5, labelanchor=N, width=100,
                                          relief=RIDGE, font=('Arial', 16, 'bold'), fg="DEEP SKY BLUE")
        my_search_labelframe.pack(pady=2, ipady=7, ipadx=20)
        my_text = Entry(my_search_labelframe, width=40, font=('Arial', 14))
        my_text.pack(pady=10)
        def search_treeview(e):
            total_items = tree.get_children()
            search = my_text.get()
            if search.lower() == "":
                updater()
            else:
                for item in total_items:
                    if search in tree.item(item)['values'][0].lower():
                        searched_result = tree.item(item)['values']
                        tree.delete(item)
                        tree.insert("",0,values=searched_result)

        tree_frame = Frame(root)
        tree_frame.pack(padx=10, expand=True)

        tree = ttk.Treeview(tree_frame, height=14)
        my_text.bind("<KeyRelease>", search_treeview)
        def fetch_corona_updates():
            clear_tree()
            global df
            url = "https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases"
            df = pd.read_html(url,header=0)
            columns = df[0][1:].columns
            tree.tag_configure('odd', background="white")
            tree.tag_configure('even', background="lightblue")
            #tree["column"] = list(columns)
            tree["column"] = list(columns)[1:]
            tree["show"] = "headings"
            for column in tree["column"]:
                tree.column(column, width=250, minwidth=95, anchor=W, stretch=YES)
                tree.heading(column, text=column, anchor=W)
            df_rows = df[0][1:].to_numpy().tolist()
            global count
            count = 0
            for row in df_rows:
                if count % 2 == 0:
                    tree.insert("", "end",values=row[1:],tags=('even',))
                else:
                    tree.insert("", "end",values=row[1:],tags=('odd',))
                count +=1
            # y scrollbar
            yscroll = ttk.Scrollbar(tree_frame, orient=VERTICAL)
            yscroll.config(command=tree.yview)
            tree.config(yscrollcommand=yscroll.set)
            yscroll.pack(fill=Y, side=RIGHT)
            # x scrollbar
            xscroll = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            xscroll.config(command=tree.xview)
            tree.config(xscrollcommand=xscroll.set)
            xscroll.pack(fill=X, side=BOTTOM)
            tree.pack()

        def updater():
            ttk.Style().theme_use('clam')
            clear_tree()
            new_df = df
            columns = new_df[0][1:].columns
            tree.tag_configure('odd', background="white")
            tree.tag_configure('even', background="lightblue")
            # tree["column"] = list(columns)
            tree["column"] = list(columns)[1:]
            tree["show"] = "headings"
            for column in tree["column"]:
                tree.column(column, width=250, minwidth=250, anchor=W, stretch=YES)
                tree.heading(column, text=column, anchor=W)
            df_rows = df[0][1:].to_numpy().tolist()
            global count
            count = 0
            for row in df_rows:
                if count % 2 == 0:
                    tree.insert("", "end", values=row[1:], tags=('even',))
                else:
                    tree.insert("", "end", values=row[1:], tags=('odd',))

                count += 1
        def clear_tree():
            tree.delete(*tree.get_children())
        fetch_corona_updates()
        root.mainloop()
    def save(self):
        import json
        with open('settings.json','r') as a_file:
            self.json_data = json.load(a_file)
            a_file.close()
            self.json_data['bg'] = self.color_combo.get()
            # self.json_data['values_to_plot_top'] =self.lab3.get()
            # self.json_data['values_to_plot_from_back'] = self.lab5.get()
        with open('settings.json','w') as written:
            json.dump(self.json_data,written,indent=2)
            written.close()
            self.root.configure(bg=self.json_data['bg'])

    #settings function
    def get_Settings(self):
        import json
        self.win = Tk()
        self.win.title('Settings')
        self.win.geometry('700x600')
        self.win.resizable(0,0)
        with open('settings.json','r') as file:
            self.data = json.load(file)
            self.colors = self.data["colors"]
            # self.from_beg = self.data['values_to_plot_top']
            # self.from_end = self.data['values_to_plot_from_back']
            self.about = self.data['about_app']
            self.version = self.data['version']
        self.cole = StringVar()
        self.lab = Label(self.win,text="Please choose a color for background.",font=('Verdana',15,'bold'))
        self.lab.pack(pady=10)
        self.color_combo = ttk.Combobox(self.win,values=self.colors,textvariable=self.cole,font=('Arial', 14), width=20)
        self.color_combo.current(0)
        self.color_combo.pack(pady=10)
        # self.lab2 = Label(self.win, text="Values to plot from start of dataframe.", font=('Verdana', 13,'bold'))
        # self.lab2.pack()
        # self.h = IntVar()
        # self.h.set(self.from_beg)
        # self.lab3 = ttk.Combobox(self.win,values=self.from_beg,textvariable=self.h,font=('Arial', 14), width=20)
        # self.lab3.current(0)
        # self.lab3.pack(pady=10)
        #
        # self.lab4 = Label(self.win, text="Values to plot from end of dataframe.", font=('Verdana', 13,'bold'))
        # self.lab4.pack()
        # self.v = IntVar()
        # self.v.set(self.from_end)
        # self.lab5 = ttk.Combobox(self.win, values=self.from_end, textvariable=self.v, font=('Arial', 14), width=20)
        # self.lab5.current(0)
        # self.lab5.pack(pady=10)
        self.lab6 = Label(self.win, text="About the App", font=('Verdana', 15,'bold'))
        self.lab6.pack(pady=5)
        self.lab7 = Label(self.win, text=self.about, font=('Verdana', 13))
        self.lab7.pack(pady=10)
        self.lab8 = Label(self.win, text="App version.", font=('Verdana', 15,'bold'))
        self.lab8.pack()
        self.lab9 = Label(self.win, text=self.version, font=('Verdana', 12))
        self.lab9.pack()
        self.btn = Button(self.win,text="Save",width=25,relief=SOLID,font=('Courier',15),command=self.save)
        self.btn.pack(pady=20)
        self.win.mainloop()

root = Tk()
app = Tkinter_dataframe_viewer(root)
root.mainloop()
