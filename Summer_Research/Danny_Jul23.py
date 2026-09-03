from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
#from matplotlib import pyplot as plt



class Controller:
   def __init__(self, master):
       self.master = master
       self.master.title('FTOF Controller GUI')
       self.master.geometry('500x300')


       self.menubar = Menu(self.master)


       self.filemenu = Menu(self.menubar, tearoff=0)
       self.aboutmenu = Menu(self.menubar, tearoff=0)
       self.helpmenu = Menu(self.menubar, tearoff=0)


       self.menubar.add_cascade(menu=self.filemenu, label='File')
       self.menubar.add_cascade(menu=self.aboutmenu, label='About')
       self.menubar.add_cascade(menu=self.helpmenu, label='Help')


       self.filemenu.add_command(label='Close', command=self.master.destroy)
       self.aboutmenu.add_command(label='About', command=self.show_about_menu)
       self.helpmenu.add_command(label='Help', command=self.show_help_menu)


       self.master.config(menu=self.menubar)


       self.about_notebook = Notebook(self.master)
       self.about_label = Label(self.about_notebook, text=
       '''about''')
       self.about_go_back_button = Button(self.about_notebook, text='Go Back To Controller',
                                          command=self.show_controller_menu)


       self.about_label.pack()
       self.about_go_back_button.pack(side=BOTTOM)


       self.help_notebook = Notebook(self.master)
       self.help_label = Label(self.help_notebook, text=
       '''help''')
       self.help_go_back_button = Button(self.help_notebook, text='Go Back To Controller',
                                          command=self.show_controller_menu)


       self.help_label.pack()
       self.help_go_back_button.pack(side=BOTTOM)


       self.controller_notebook = Notebook(self.master)
       self.tab1 = Frame(self.controller_notebook)
       self.tab1_layout = Frame(self.tab1)
       vcmd = master.register(self.int_checker)
       self.run_number_label = Label(self.tab1_layout, text='Run Number')
       self.entry_box = Spinbox(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'), from_=1,
                                to=999999999, increment=1)
       self.min_files_label = Label(self.tab1_layout, text='Minimum Files Before Graphing')
       self.min_files_entry = Entry(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'))
       self.get_data_button = Button(self.tab1_layout, text='Retrieve FTOF Data From Run Number', state=DISABLED,
                                    command=self.get_data)
       self.run_data_button = Button(self.tab1_layout, text='Graph FTOF Efficiency Data', command=self.run_data,
                                state=DISABLED)


       self.tab2 = Frame(self.controller_notebook)
       self.tab2_text = Label(self.tab2, text='Graphs')


       self.message_box_text = StringVar()
       self.message_box_text.set('')
       self.message_box = Label(master, textvariable=self.message_box_text, padding=[30, 0, 30, 40])


       self.get_data_button.grid(row=1, column=0,pady=5)
       self.run_number_label.grid(row=0, column=1)
       self.entry_box.grid(row=1, column=1)
       self.run_data_button.grid(row=3, column=0)
       self.min_files_label.grid(row=2, column=1)
       self.min_files_entry.grid(row=3, column=1)
       self.tab1_layout.pack(pady=20)
       self.tab2_text.pack()
       self.tab1.pack()
       self.tab2.pack()


       self.controller_notebook.add(self.tab1, text='Data Retrieval')
       self.controller_notebook.add(self.tab2, text='FTOF Graphs')


       self.controller_notebook.pack(expand=True, fill=BOTH, padx=20, pady=20)
       self.message_box.pack(anchor=W)


       def button_enabler(event):
           if len(self.entry_box.get()) >= 1:
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
       self.run_number = self.entry_box.get()
       if int(self.run_number) > 0:
           self.min_files = self.min_files_entry.get()
           if self.min_files == '':
               self.min_files = 'ALL'
           self.message_box_text.set('Data was definitely retrieved from run number ' + str(self.run_number) + '.'
                                     + '\n' + 'Minimum number of files retrieved before graphing is ' +
                                     self.min_files + ' files.')
           self.run_data_button.configure(state=NORMAL)
           self.get_data_button.configure(state=DISABLED)
           self.entry_box.delete(0, END)
       else:
           self.message_box_text.set('Input a run number greater than 0.')


   def run_data(self):
       self.message_box_text.set('Data from run number ' + str(self.run_number) + ' was definitely graphed.')
       self.run_data_button.configure(state=DISABLED)


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


root = Tk()
Controller_GUI = Controller(root)
root.mainloop()

