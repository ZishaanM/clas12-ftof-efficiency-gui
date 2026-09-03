from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import webbrowser
import subprocess
import glob
from time import sleep
import pandas as pd
from pandasgui import show
import json
import os


class Controller:
   def __init__(self, master):
       #defining master object
       self.master = master
       self.master.title('FTOF Controller GUI')
       self.master.geometry('800x500')


       #menubar objects (file, menu, help)
       self.menubar = Menu(self.master)


       self.filemenu = Menu(self.menubar, tearoff=0)
       self.aboutmenu = Menu(self.menubar, tearoff=0)
       self.helpmenu = Menu(self.menubar, tearoff=0)


       self.menubar.add_cascade(menu=self.filemenu, label='File')
       self.menubar.add_cascade(menu=self.aboutmenu, label='About')
       self.menubar.add_cascade(menu=self.helpmenu, label='Help')


       self.filemenu.add_command(label='Close', command=self.close_window)
       self.aboutmenu.add_command(label='About', command=self.show_about_menu)
       self.helpmenu.add_command(label='Help', command=self.show_help_menu)


       self.master.config(menu=self.menubar)


       #about menubar
       self.about_notebook = Notebook(self.master)
       self.about_label = Label(self.about_notebook, text=
       '''about''')
       self.go_to_website = Button(self.about_notebook, text='Link To More Information',
                                          command=self.open_website)
       self.about_go_back_button = Button(self.about_notebook, text='Go Back To Controller',
                                          command=self.show_controller_menu)


       self.about_label.pack()
       self.about_go_back_button.pack(side=BOTTOM)
       self.go_to_website.pack(side=BOTTOM)


       #help menubar
       self.help_notebook = Notebook(self.master)
       self.help_label = Label(self.help_notebook, text=
       '''help''')
       self.help_go_back_button = Button(self.help_notebook, text='Go Back To Controller',
                                          command=self.show_controller_menu)


       self.help_label.pack()
       self.help_go_back_button.pack(side=BOTTOM)


       #data retrieval notebook
       self.controller_notebook = Notebook(self.master)
       self.tab1 = Frame(self.controller_notebook)
       self.tab1_layout = Frame(self.tab1)
       vcmd = master.register(self.int_checker)
       self.run_number_label = Label(self.tab1_layout, text='Run Number')
       self.run_number_entry = Spinbox(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'), from_=1,
                                to=999999999, increment=1)
       self.min_files_label = Label(self.tab1_layout, text='Minimum Files Before Graphing')
       self.min_files_entry = Spinbox(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'), from_=1,
                                to=999999999, increment=1)
       self.get_data_button = Button(self.tab1_layout, text='Retrieve FTOF Data From Run Number', state=DISABLED,
                                    command=self.get_data)
       self.graph_data_button = Button(self.tab1_layout, text='Graph FTOF Efficiency Data', command=self.graph_data,
                                state=DISABLED)


       #sector, layer, topology checkboxes
       self.var = {i: IntVar() for i in range(1, 15)}  # Supports sectors 1-6 and topologies 7-11
       self.choose_sector_label = Label(self.tab1_layout, text='SECTOR')
       self.choose_sector1 = Checkbutton(self.tab1_layout, text='Sector 1', variable=self.var[1])
       self.choose_sector2 = Checkbutton(self.tab1_layout, text='Sector 2', variable=self.var[2])
       self.choose_sector3 = Checkbutton(self.tab1_layout, text='Sector 3', variable=self.var[3])
       self.choose_sector4 = Checkbutton(self.tab1_layout, text='Sector 4', variable=self.var[4])
       self.choose_sector5 = Checkbutton(self.tab1_layout, text='Sector 5', variable=self.var[5])
       self.choose_sector6 = Checkbutton(self.tab1_layout, text='Sector 6', variable=self.var[6])
       self.choose_topology_label = Label(self.tab1_layout, text='TOPOLOGY')
       self.choose_topology1 = Checkbutton(self.tab1_layout, text='Topology 1', variable=self.var[10])
       self.choose_topology2 = Checkbutton(self.tab1_layout, text='Topology 2', variable=self.var[11])
       self.choose_topology3 = Checkbutton(self.tab1_layout, text='Topology 3', variable=self.var[12])
       self.choose_topology4 = Checkbutton(self.tab1_layout, text='Topology 4', variable=self.var[13])
       self.choose_topology5 = Checkbutton(self.tab1_layout, text='Topology 5', variable=self.var[14])
       self.choose_layer_label = Label(self.tab1_layout, text='LAYER')
       self.choose_layer1 = Checkbutton(self.tab1_layout, text='Layer 1', variable=self.var[7])
       self.choose_layer2 = Checkbutton(self.tab1_layout, text='Layer 2', variable=self.var[8])
       self.choose_layer3 = Checkbutton(self.tab1_layout, text='Layer 3', variable=self.var[9])


       #overlay options
       self.overlay_value = StringVar()
       self.overlayList = ['None', 'None', 'Sector', 'Layer', 'Topology']
       self.overlay_menu = OptionMenu(self.tab1_layout, self.overlay_value, *self.overlayList)


       #graphing notebook
       self.tab2 = Frame(self.controller_notebook)
       # self.pandasgui_button = Button(self.tab2, text='Show Graphs', state=DISABLED, command=self.open_pandasgui)
       # self.renew_button = Button(self.tab2, text='Clear Entries To Retrieve Another Run Number', state=DISABLED,
       #                            command=self.clear_entries)


       #messagebox
       #self.message_box_text = StringVar()
       #self.message_box_text.set('')
       #self.message_box = Label(master, textvariable=self.message_box_text, padding=[30, 0, 30, 40])


       #data retrieval notebook layout
       self.get_data_button.grid(row=1, column=0,pady=5)
       self.run_number_label.grid(row=0, column=1)
       self.run_number_entry.grid(row=1, column=1)
       self.graph_data_button.grid(row=3, column=0)
       self.min_files_label.grid(row=2, column=1)
       self.min_files_entry.grid(row=3, column=1)
       self.tab1_layout.pack(pady=20)
       # self.pandasgui_button.pack()
       # self.renew_button.pack()
       self.tab1.pack()
       self.tab2.pack()
       #checkboxes in data retrieval layout
       self.tab1_layout.grid_rowconfigure(4, weight=1000)
       self.choose_sector_label.grid(row=5, column=0)
       self.choose_sector1.grid(row=6, column=0)
       self.choose_sector2.grid(row=7, column=0)
       self.choose_sector3.grid(row=8, column=0)
       self.choose_sector4.grid(row=9, column=0)
       self.choose_sector5.grid(row=10, column=0)
       self.choose_sector6.grid(row=11, column=0)
       self.choose_topology_label.grid(row=5, column=2)
       self.choose_topology1.grid(row=6, column=2)
       self.choose_topology2.grid(row=7, column=2)
       self.choose_topology3.grid(row=8, column=2)
       self.choose_topology4.grid(row=9, column=2)
       self.choose_topology5.grid(row=10, column=2)
       self.choose_layer_label.grid(row=5, column=1)
       self.choose_layer1.grid(row=6, column=1)
       self.choose_layer2.grid(row=7, column=1)
       self.choose_layer3.grid(row=8, column=1)


       self.overlay_menu.grid(row=6, column=4)


       self.controller_notebook.add(self.tab1, text='Data Retrieval & Graphing')
       self.controller_notebook.add(self.tab2, text='Complex Graphing')


       self.controller_notebook.pack(expand=True, fill=BOTH, padx=20, pady=20)
       #self.message_box.pack(anchor=W)


       def button_enabler(event):
           if len(self.run_number_entry.get()) >= 1:
               self.get_data_button.configure(state=NORMAL)
           else:
               self.get_data_button.configure(state=DISABLED)
       self.master.bind('<KeyRelease>', button_enabler)
       self.master.bind('<ButtonPress>', button_enabler)
       self.master.protocol('WM_DELETE_WINDOW', self.close_window)


   def int_checker(self, P):
       if str.isdigit(P) or P == "":
           return True
       else:
           return False


   def get_data(self):
       self.run_number = self.run_number_entry.get()
       if int(self.run_number) > 0:
           self.min_files = self.min_files_entry.get()
           if self.min_files == '':
               self.min_files = 'ALL'
           self.graph_data_button.configure(state=NORMAL)
           self.get_data_button.configure(state=DISABLED)
           self.run_number_entry.delete(0, END)
           #update textbox
           self.in_progress()
           #run other script to retrieve data
           #don't have this right now
           #check for right number of files
           #self.check_files() (disabled for now)
           self.min_files_entry.configure(state=DISABLED)
           self.run_number_entry.configure(state=DISABLED)
           self.run_MakeData()
       #else:
           #self.message_box_text.set('Input a run number greater than 0.')


   def get_cbox_vals(self):
       self.sectorList = []
       self.layerList = []
       self.topologyList = []
       for i in range(1, 15):
           temp = self.var[i].get()
           if temp != 0:
               if 1 <= i <= 6:
                   self.sectorList.append(i)
               elif 7 <= i <= 9:
                   self.layerList.append(i - 6)
               elif 10 <= i <= 14:
                   self.topologyList.append(i - 9)


   def graph_data(self):
       self.get_cbox_vals()
       #self.message_box_text.set('Data from run number ' + str(self.run_number) + ' was definitely graphed.')
       #script to refine data and make graphs
       self.run_GraphData()
       self.graph_data_button.configure(state=DISABLED)
       #self.pandasgui_button.configure(state=NORMAL)
       self.df = pd.read_csv(r'C:\Users\zisha\SynologyDrive\Drive\Tkinter_GUI\CSV\rga_all.csv')
       #self.df = pd.read_csv('CSVs/rga_all.csv')


   def run_MakeData(self):
       #subprocess.run(['python', 'CreateTestFiles.py'])
       subprocess.run(['python', 'MakeData_Jan24.py', str(self.run_number)],
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


   def find_overlay(self):
       self.overlay = self.overlay_value.get()
       if self.overlay == 'None':
           self.ol_secs = 'False'
           self.ol_lys = 'False'
           self.ol_tops = 'False'
       elif self.overlay == 'Sector':
           self.ol_secs = 'True'
           self.ol_lys = 'False'
           self.ol_tops = 'False'
       elif self.overlay == 'Topology':
           self.ol_secs = 'False'
           self.ol_lys = 'False'
           self.ol_tops = 'True'
       if self.overlay == 'Layer':
           self.ol_secs = 'False'
           self.ol_lys = 'True'
           self.ol_tops = 'False'


   def run_GraphData(self):
       self.find_overlay()
       self.ser_sectors = json.dumps(self.sectorList)
       self.ser_topologies = json.dumps(self.topologyList)
       self.ser_layers = json.dumps(self.layerList)
       subprocess.run(['python', 'GraphData_Jan24.py', str(self.run_number), self.ser_sectors, self.ser_layers,
                       self.ser_topologies, self.ol_secs, self.ol_lys, self.ol_tops], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


   def close_window(self):
       if messagebox.askyesno(title='Quit?', message='Close Window?'):
           self.master.destroy()


   def show_about_menu(self):
       self.message_box.pack_forget()
       self.controller_notebook.pack_forget()
       self.help_notebook.pack_forget()
       self.about_notebook.pack(expand=True, fill=BOTH, padx=20, pady=20)
       self.message_box.pack(anchor=W)


   def show_help_menu(self):
       self.message_box.pack_forget()
       self.controller_notebook.pack_forget()
       self.about_notebook.pack_forget()
       self.help_notebook.pack(expand=True, fill=BOTH, padx=20, pady=20)
       self.message_box.pack(anchor=W)


   def show_controller_menu(self):
       self.message_box.pack_forget()
       self.about_notebook.pack_forget()
       self.help_notebook.pack_forget()
       self.controller_notebook.pack(expand=True, fill=BOTH, padx=20, pady=20)
       self.message_box.pack(anchor=W)


   def open_website(self):
       webbrowser.open_new('https://www.jlab.org/physics/hall-b/clas12')


   def in_progress(self):
       #self.message_box_text.set('Data retrieval is IN PROGRESS from run number ' + str(self.run_number) + '.'
                                 #+ '\n' + 'Minimum number of files retrieved before graphing is ' +
                                 #self.min_files + ' files.')
       self.master.update_idletasks()


   def check_files(self):
       self.directory = '../GUI/PracticeFiles/'
       self.files = glob.glob(self.directory + '*')
       if self.min_files == 'ALL':
           self.check = 10
       else:
           self.check = self.min_files
       while len(self.files) < self.check:
           self.files = glob.glob(self.directory + '*')
           sleep(1)
       #if len(self.files) >= self.check:
           #self.message_box_text.set('Data successfully retrieved from run number ' + str(self.run_number) + '.')


   def open_pandasgui(self):
       show(self.df)
       #self.renew_button.configure(state=NORMAL)


   def clear_entries(self):
       self.min_files_entry.configure(state=NORMAL)
       self.run_number_entry.configure(state=NORMAL)
       #self.pandasgui_button.configure(state=DISABLED)
       #self.renew_button.configure(state=DISABLED)




root = Tk()
Controller_GUI = Controller(root)
root.mainloop()
