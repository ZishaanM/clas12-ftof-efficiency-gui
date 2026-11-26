import os
import sys
import json
import glob
import subprocess
import webbrowser
from time import sleep
from tkinter import messagebox, Menu, IntVar, StringVar, DISABLED, NORMAL, END  # Only import what's needed

import pandas as pd
import customtkinter as ctk
from scipy.stats import ks_2samp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.environ.get('FTOF_OUTPUT_DIR', os.path.join(BASE_DIR, 'output'))

class Controller:
    def open_website(self):
        webbrowser.open("https://www.jlab.org/physics/hall-b/clas12")

    def __init__(self, master):
        ctk.set_appearance_mode("dark")  # Dark mode


        self.master = master
        self.master.title('FTOF Controller GUI')
        self.master.geometry('1000x700')
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Menu Bar
        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.aboutmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.menubar.add_cascade(label='About', menu=self.aboutmenu)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)
        self.filemenu.add_command(label='Close', command=self.close_window)
        self.aboutmenu.add_command(label='About', command=self.show_about_menu)
        self.helpmenu.add_command(label='Help', command=self.show_help_menu)
        #self.master.config(menu=self.menubar)

        # Controller Notebook
        self.controller_notebook = ctk.CTkTabview(self.master)
        self.controller_notebook.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.controller_notebook.add("Controller")

        self.message_box_text = StringVar()
        self.message_box = ctk.CTkLabel(self.master, textvariable=self.message_box_text)
        self.message_box.grid(row=0, column=0, sticky="w", padx=5, pady=5)



        
        self.about_notebook = ctk.CTkTabview(self.master)

        self.about_label = ctk.CTkLabel(self.about_notebook, text=
       '''about''')
        self.go_to_website = ctk.CTkButton(self.about_notebook, text='Link To More Information',
                                          command=self.open_website)
        self.about_go_back_button = ctk.CTkButton(self.about_notebook, text='Go Back To Controller',
                                          command=self.show_controller_menu)
        
        self.about_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.about_go_back_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.go_to_website.grid(row=2, column=0, padx=5, pady=5, sticky="ew")


       #help menubar
        self.help_notebook = ctk.CTkTabview(self.master)
        self.help_label = ctk.CTkLabel(self.help_notebook, text=
       '''help''')
        self.help_go_back_button = ctk.CTkButton(self.help_notebook, text='Go Back To Controller',
                                          command=self.show_controller_menu)


        self.help_label.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.help_go_back_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        #----------------------------------------------------



        # Layout Frame inside Controller Tab
        self.tab1_layout = ctk.CTkFrame(self.controller_notebook.tab("Controller"))
        self.tab1_layout.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.spacer = ctk.CTkLabel(self.tab1_layout, text="", width=230, height=10)  # Adjust width/height as needed
        self.spacer.grid(row=0, column=0,padx=5, pady=5)

        vcmd = self.master.register(self.int_checker)
        self.run_number_label = ctk.CTkLabel(self.tab1_layout, text='Run Number')
        self.run_number_entry = ctk.CTkEntry(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'))
        self.min_files_label = ctk.CTkLabel(self.tab1_layout, text='Minimum Files Before Graphing')
        self.min_files_entry = ctk.CTkEntry(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'))
        self.get_data_button = ctk.CTkButton(self.tab1_layout, text='Retrieve FTOF Data From Run Number',
                                             state='disabled', command=self.get_data)
        self.graph_data_button = ctk.CTkButton(self.tab1_layout, text='Graph FTOF Efficiency Data',
                                               state='disabled', command=self.graph_data)
        
        self.get_data_button.grid(row=1, column=1, padx=5, pady=5)
        self.run_number_label.grid(row=0, column=2, padx=5, pady=5)
        self.run_number_entry.grid(row=1, column=2, padx=5, pady=5)
        self.graph_data_button.grid(row=3, column=1, padx=5, pady=5)
        self.min_files_label.grid(row=2, column=2, padx=5, pady=5)
        self.min_files_entry.grid(row=3, column=2, padx=5, pady=5)

        # Checkboxes for Sector, Layer, Topology
        self.var = {i: IntVar() for i in range(1, 15)}
        self.choose_sector_label = ctk.CTkLabel(self.tab1_layout, text='SECTOR')
        self.choose_sector1 = ctk.CTkCheckBox(self.tab1_layout, text='Sector 1', variable=self.var[1])
        self.choose_sector2 = ctk.CTkCheckBox(self.tab1_layout, text='Sector 2', variable=self.var[2])
        self.choose_sector3 = ctk.CTkCheckBox(self.tab1_layout, text='Sector 3', variable=self.var[3])
        self.choose_sector4 = ctk.CTkCheckBox(self.tab1_layout, text='Sector 4', variable=self.var[4])
        self.choose_sector5 = ctk.CTkCheckBox(self.tab1_layout, text='Sector 5', variable=self.var[5])
        self.choose_sector6 = ctk.CTkCheckBox(self.tab1_layout, text='Sector 6', variable=self.var[6])
        self.choose_topology_label = ctk.CTkLabel(self.tab1_layout, text='TOPOLOGY')
        self.choose_topology1 = ctk.CTkCheckBox(self.tab1_layout, text='Topology 1', variable=self.var[10])
        self.choose_topology2 = ctk.CTkCheckBox(self.tab1_layout, text='Topology 2', variable=self.var[11])
        self.choose_topology3 = ctk.CTkCheckBox(self.tab1_layout, text='Topology 3', variable=self.var[12])
        self.choose_topology4 = ctk.CTkCheckBox(self.tab1_layout, text='Topology 4', variable=self.var[13])
        self.choose_topology5 = ctk.CTkCheckBox(self.tab1_layout, text='Topology 5', variable=self.var[14])
        self.choose_layer_label = ctk.CTkLabel(self.tab1_layout, text='LAYER')
        self.choose_layer1 = ctk.CTkCheckBox(self.tab1_layout, text='Layer 1', variable=self.var[7])
        self.choose_layer2 = ctk.CTkCheckBox(self.tab1_layout, text='Layer 2', variable=self.var[8])
        self.choose_layer3 = ctk.CTkCheckBox(self.tab1_layout, text='Layer 3', variable=self.var[9])


        self.choose_sector_label.grid(row=5, column=1, padx=5, pady=5)
        self.choose_sector1.grid(row=6, column=1, padx=5, pady=5)
        self.choose_sector2.grid(row=7, column=1, padx=5, pady=5)
        self.choose_sector3.grid(row=8, column=1, padx=5, pady=5)
        self.choose_sector4.grid(row=9, column=1, padx=5, pady=5)
        self.choose_sector5.grid(row=10, column=1, padx=5, pady=5)
        self.choose_sector6.grid(row=11, column=1, padx=5, pady=5)
        self.choose_topology_label.grid(row=5, column=3)
        self.choose_topology1.grid(row=6, column=3)
        self.choose_topology2.grid(row=7, column=3)
        self.choose_topology3.grid(row=8, column=3)
        self.choose_topology4.grid(row=9, column=3)
        self.choose_topology5.grid(row=10, column=3)
        self.choose_layer_label.grid(row=5, column=2)
        self.choose_layer1.grid(row=6, column=2)
        self.choose_layer2.grid(row=7, column=2)
        self.choose_layer3.grid(row=8, column=2)

        
        self.overlay_value = StringVar(value='Overlay Setting')
        self.overlayList = ['None', 'Sector', 'Layer', 'Topology']
        self.overlay_menu = ctk.CTkOptionMenu(self.tab1_layout, variable=self.overlay_value, values=self.overlayList)
        self.overlay_menu.grid(row=3, column=3, padx=20, pady=5)



        #tab 2: Complex Graphing
        self.controller_notebook.add("KS Test")
        self.tab2 = ctk.CTkFrame(self.controller_notebook.tab("KS Test"))
        self.tab2.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)


        self.spacer2 = ctk.CTkLabel(self.tab2, text="", width=420, height=10)  # Adjust width/height as needed
        self.spacer2.grid(row=0, column=0,padx=5, pady=5)


        # Free-text boxes
        self.run1_entry = ctk.CTkEntry(self.tab2, placeholder_text="Run Number 1")
        self.run1_entry.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        self.run2_entry = ctk.CTkEntry(self.tab2, placeholder_text="Run Number 2")
        self.run2_entry.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.tab2, text="Run Number 1:").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.tab2, text="Run Number 2:").grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.alternateOptions = ["two-sided", "less", "greater"]
        self.methodOptions = ["auto", "exact", "asymptotic"]
        self.axisOptions = [0, 1, "None"]
        self.axis_value_map = {str(val): val for val in self.axisOptions}
        self.nanOptions = ["propagate", "raise", "omit"]
        self.keepdimsOptions = ["True", "False"]


        self.alternative_dropdown = ctk.CTkComboBox(self.tab2, values=self.alternateOptions)
        self.alternative_dropdown.set(self.alternateOptions[0])
        self.alternative_dropdown.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        self.method_dropdown = ctk.CTkComboBox(self.tab2, values=self.methodOptions)
        self.method_dropdown.set(self.methodOptions[0])
        self.method_dropdown.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

        self.axis_dropdown = ctk.CTkComboBox(self.tab2, values=list(self.axis_value_map.keys()))
        self.axis_dropdown.set(str(self.axisOptions[0]))
        self.axis_dropdown.grid(row=4, column=2, padx=10, pady=5, sticky="ew")

        self.nan_policy_dropdown = ctk.CTkComboBox(self.tab2, values=self.nanOptions)
        self.nan_policy_dropdown.set(self.nanOptions[0])
        self.nan_policy_dropdown.grid(row=5, column=2, padx=10, pady=5, sticky="ew")

        self.keepdims_dropdown = ctk.CTkComboBox(self.tab2, values=self.keepdimsOptions)
        self.keepdims_dropdown.set(self.keepdimsOptions[1])
        self.keepdims_dropdown.grid(row=6, column=2, padx=10, pady=5, sticky="ew")

        # Labels for dropdowns
        ctk.CTkLabel(self.tab2, text="Alternative:").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.tab2, text="Method:").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.tab2, text="Axis:").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.tab2, text="NaN Policy:").grid(row=5, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.tab2, text="Keepdims:").grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Efficiency options (strings to prevent ljust() error)
        efficiency_options = ["All", "1", "2", "3", "4", "5"]

        # Efficiency 1 dropdown
        ctk.CTkLabel(self.tab2, text="Efficiencies to Compare:").grid(row=8, column=1, padx=10, pady=5)
        self.efficiency_dropdown = ctk.CTkComboBox(self.tab2, values=efficiency_options)
        self.efficiency_dropdown.set(efficiency_options[0])  # Default value
        self.efficiency_dropdown.grid(row=8, column=2, padx=10, pady=5, sticky="ew")

        self.significance_label = ctk.CTkLabel(self.tab2, text="Significance Level: ")
        self.significance_label.grid(row=7, column=1, padx=10, pady=5, sticky="w")
        self.significance_input = ctk.CTkEntry(self.tab2)
        self.significance_input.grid(row=7, column=2, padx=10, pady=5, sticky="ew")

        self.calculate_button = ctk.CTkButton(self.tab2, text="Calculate", command=self.KS_test, text_color="white")
        self.calculate_button.grid(row=9, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

        def button_enabler(event=None):
            # Enable button1 if entry has text
            if self.run_number_entry.get().strip():
                self.get_data_button.configure(state="normal")
            else:
                self.get_data_button.configure(state="disabled")

            # Enable button2 if it's clicked
            if event and event.widget == self.graph_data_button:
                self.graph_data_button.configure(state="normal")
        self.get_data_button.bind('<ButtonPress>', button_enabler)
        self.graph_data_button.bind('<ButtonPress>', button_enabler)
        self.run_number_entry.bind('<KeyRelease>', button_enabler)
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)

    def wide_csv_path(self, run_number):
        return os.path.join(OUTPUT_DIR, f'ftof_eff_{run_number}_wide.csv')

    def load_efficiencies(self, run_number, efficiency):
        path = self.wide_csv_path(run_number)
        if not os.path.exists(path):
            subprocess.run([sys.executable, os.path.join(BASE_DIR, 'MakeData_Jan24.py'), run_number])
        df = pd.read_csv(path)
        if efficiency == 'All':
            columns = [f'ef_{n}' for n in range(1, 6)]
        else:
            columns = [f'ef_{efficiency}']
        return df[columns].to_numpy().ravel()

    def KS_test(self):
        run1 = self.run1_entry.get().strip()
        run2 = self.run2_entry.get().strip()
        try:
            efficiency = self.efficiency_dropdown.get()
            self.data1 = self.load_efficiencies(run1, efficiency)
            self.data2 = self.load_efficiencies(run2, efficiency)
        except (FileNotFoundError, KeyError):
            self.message_box_text.set(f"Error: could not load efficiency data for runs '{run1}' and '{run2}'.")
            return
        self.alternative = self.alternative_dropdown.get()
        self.method = self.method_dropdown.get()
        self.axis = self.axis_value_map[self.axis_dropdown.get()]
        self.nan_policy = self.nan_policy_dropdown.get()
        self.keepdims = self.keepdims_dropdown.get() == "True"
        self.KS = ks_2samp(self.data1, self.data2, alternative=self.alternative, method=self.method, axis=self.axis, nan_policy=self.nan_policy, keepdims=self.keepdims)
        self.pval = self.KS.pvalue
        self.test_stat = self.KS.statistic
        self.alpha_str = self.significance_input.get().strip()  # Remove any extra spaces
        if self.alpha_str == "":  
            alpha = 0.05
        else:
            try:
                alpha = float(self.alpha_str)  # Convert to float
            except ValueError:
                self.message_box_text.set("Error: Invalid significance level. Please enter a valid number.")
                return
        if alpha > self.pval:
            self.message_box_text.set(f"KS Test Statistic: {self.test_stat}\nP-Value: {self.pval}\nRuns likely come from different distributions")
        else:
            self.message_box_text.set(f"KS Test Statistic: {self.test_stat}\nP-Value: {self.pval}\nNo significant difference between runs")

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
       else:
           self.message_box_text.set('Input a run number greater than 0.')


    

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
       #script to refine data and make graphs
       result = self.run_GraphData()
       if result.returncode == 0:
           self.message_box_text.set('Data from run number ' + str(self.run_number) + ' was graphed (see PDFs/).')
       else:
           print(result.stderr)
           self.message_box_text.set('Graphing failed for run number ' + str(self.run_number) + '. See console output.')
       self.graph_data_button.configure(state=DISABLED)


    def run_MakeData(self):
       print("MakeData was run, Controller")
       #subprocess.run(['python', 'MakeData_Jan24.py', str(self.run_number)],
                      #stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
       subprocess.run([sys.executable, os.path.join(BASE_DIR, 'MakeData_Jan24.py'), str(self.run_number)])


    def find_overlay(self):
       self.overlay = self.overlay_value.get()
       if self.overlay not in self.overlayList:
           self.overlay = 'None'
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
       return subprocess.run([sys.executable, os.path.join(BASE_DIR, 'GraphData_Jan24.py'), str(self.run_number),
                              self.ser_sectors, self.ser_layers, self.ser_topologies,
                              self.ol_secs, self.ol_lys, self.ol_tops],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
       #subprocess.run(['python', 'GraphData_Jan24.py', str(self.run_number), self.ser_sectors, self.ser_layers,
                       #self.ser_topologies, self.ol_secs, self.ol_lys, self.ol_tops])


    def close_window(self):
       if messagebox.askyesno(title='Quit?', message='Close Window?'):
           self.master.destroy()


    def show_about_menu(self):
       self.message_box.pack_forget()
       self.controller_notebook.pack_forget()
       self.help_notebook.pack_forget()
       self.about_notebook.pack(expand=True, fill=BOTH, padx=20, pady=20)
       #self.message_box.pack(anchor=W)


    def show_help_menu(self):
       self.message_box.pack_forget()
       self.controller_notebook.pack_forget()
       self.about_notebook.pack_forget()
       self.help_notebook.pack(expand=True, fill=BOTH, padx=20, pady=20)
       #self.message_box.pack(anchor=W)


    def show_controller_menu(self):
       self.message_box.pack_forget()
       self.about_notebook.pack_forget()
       self.help_notebook.pack_forget()
       self.controller_notebook.pack(expand=True, fill=BOTH, padx=20, pady=20)
       #self.message_box.pack(anchor=W)


    def open_website(self):
       webbrowser.open_new('https://www.jlab.org/physics/hall-b/clas12')


    def in_progress(self):
       self.message_box_text.set('Data retrieval is IN PROGRESS from run number ' + str(self.run_number) + '.'
                                 + '\n' + 'Minimum number of files retrieved before graphing is ' +
                                 self.min_files + ' files.')
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
       if len(self.files) >= self.check:
           self.message_box_text.set('Data successfully retrieved from run number ' + str(self.run_number) + '.')


    def open_pandasgui(self):
       from pandasgui import show
       show(pd.read_csv(self.wide_csv_path(self.run_number)))
       #self.renew_button.configure(state=NORMAL)


    def clear_entries(self):
       self.min_files_entry.configure(state=NORMAL)
       self.run_number_entry.configure(state=NORMAL)
       #self.pandasgui_button.configure(state=DISABLED)
       #self.renew_button.configure(state=DISABLED)

if __name__ == "__main__":
    root = ctk.CTk()
    Controller_GUI = Controller(root)
    root.mainloop()