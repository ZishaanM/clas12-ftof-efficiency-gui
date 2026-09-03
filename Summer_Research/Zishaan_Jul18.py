from tkinter import *
from tkinter.ttk import *
from matplotlib import pyplot as plt
from tkinter import messagebox




class Controller:
   def __init__(self, master):
       self.master = master
       self.master.geometry('500x300')


       self.menubar = Menu(self.master)
       self.master.config(menu=self.menubar)

       self.filemenu = Menu(self.menubar, tearoff=0)
       self.aboutmenu = Menu(self.menubar, tearoff=0)
       self.helpmenu = Menu(self.menubar, tearoff=0)

       self.menubar.add_cascade(menu=self.filemenu, label='File')
       self.menubar.add_cascade(menu=self.aboutmenu, label='About')
       self.menubar.add_cascade(menu=self.helpmenu, label='Help')

       self.filemenu.add_command(label='Close', command=exit)
       self.aboutmenu.add_command(label='About')
       self.helpmenu.add_command(label='Help')
       self.master.config(menu=self.menubar)




       self.title = Label(master, text='Controller GUI')
       self.notebook = Notebook(master, padding=[30, 10, 30, 0])
       self.message_box_text = StringVar()
       self.message_box_text.set('')
       self.message_box = Label(master, textvariable=self.message_box_text, padding=[30, 30, 30, 40])




       self.tab1 = Frame(self.notebook)
       self.tab1_layout = Frame(self.tab1)
       vcmd = master.register(self.int_checker)
       self.run_number_label = Label(self.tab1_layout, text='Run Number')
       self.entry_box = Spinbox(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'), from_=1,
                                to=999999999, increment=1)
       self.min_files_label = Label(self.tab1_layout, text='Minimum files')
       self.min_files_entry = Entry(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'))
       self.get_data_button = Button(self.tab1_layout, text='Retrieve FTOF Data From Run Number', state=DISABLED,
                                    command=self.get_data)
       self.run_data_button = Button(self.tab1_layout, text='Graph FTOF Efficiency Data', command=self.run_data,
                                state=DISABLED)




       self.tab2 = Frame(self.notebook)
       self.tab2_text = Label(self.tab2, text='test2')




       self.get_data_button.grid(row=1, column=0,pady=5)
       self.run_number_label.grid(row=0, column=1)
       self.min_files_label.grid(row=2, column=1)
       self.entry_box.grid(row=1, column=1)
       self.run_data_button.grid(row=2, column=0)
       self.min_files_entry.grid(row=3, column=1)
       self.tab1_layout.pack(pady=20)
       self.tab2_text.pack()
       self.tab1.pack()
       self.tab2.pack()




       self.notebook.add(self.tab1, text='Data Retrieval')
       self.notebook.add(self.tab2, text='Window2')




       self.title.pack()
       self.notebook.pack(expand=True, fill=BOTH)
       self.message_box.pack(anchor=W, side=TOP)


       self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

       def switch_tab(event):
           pass

       def button_enabler(event):
           if len(self.entry_box.get()) >= 1:
               self.get_data_button.configure(state=NORMAL)
           else:
               self.get_data_button.configure(state=DISABLED)
       self.master.bind('<KeyRelease>', button_enabler)
       self.master.bind('<ButtonPress>', button_enabler)
   def int_checker(self, P):
       if str.isdigit(P) or P == "":
           return True
       else:
           return False




   def get_data(self):
       self.run_number = self.entry_box.get()
       if int(self.run_number) > 0:
           min_files = self.min_files_entry.get()
           print(min_files)
           if min_files == "":
               min_files = "ALL"
           readout = "Minimum number of files retrieved before graphing is " + min_files + " files."
           self.message_box_text.set('Data was definitely retrieved from run number ' +
           str(self.run_number) + '.' + '\n' + readout)
           self.run_data_button.configure(state=NORMAL)
           self.get_data_button.configure(state=DISABLED)
           self.entry_box.delete(0, END)
       else:
           self.message_box_text.set('Input a run number greater than 0.')


   def on_closing(self):
       if messagebox.askyesno(title="Quit?", message="Close window?"):
           self.master.destroy()


   def run_data(self):
       self.message_box_text.set('Data from run number ' + str(self.run_number) + ' was definitely graphed.')
       self.run_data_button.configure(state=DISABLED)




root = Tk()
Controller_GUI = Controller(root)
root.mainloop()
