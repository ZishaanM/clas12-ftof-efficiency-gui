from tkinter import *
from tkinter.ttk import *
from matplotlib import pyplot as plt



class Controller:
    def __init__(self, master):
        self.master = master
        self.master.geometry('500x300')

        self.title = Label(master, text='Controller GUI')
        self.notebook = Notebook(master, padding=[30, 10, 30, 0])
        self.message_box_text = StringVar()
        self.message_box_text.set('')
        self.message_box = Label(master, textvariable=self.message_box_text, padding=[30, 30, 30, 40])

        self.tab1 = Frame(self.notebook)
        self.tab1_layout = Frame(self.tab1)
        vcmd = master.register(self.int_checker)
        self.run_number_label = Label(self.tab1_layout, text='Type Run Number Below')
        # Zishaan edit (scroll ability). Turned entry_box widget from entry to spinbox, then added from/to limits and increment
        self.entry_box = Spinbox(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'), from_=0, to=999999999, increment=1)
        self.get_data_button = Button(self.tab1_layout, text='Retrieve FTOF Data From Run Number', state=DISABLED,
                                     command=self.get_data)
        self.run_data_button = Button(self.tab1_layout, text='Graph FTOF Efficiency Data', command=self.run_data,
                                 state=DISABLED)
        # Zishaan addition. Not sure what else to add in here. Especially since I don't know what is in the entry_box widget. Can I make it strictly integer input?
        self.min_files_entry = Entry(self.tab1_layout, validate='all', validatecommand=(vcmd, '%P'))
        self.min_files_entry.insert(0, self.entry_box.cget)

        self.tab2 = Frame(self.notebook)
        self.tab2_text = Label(self.tab2, text='test2')

        self.get_data_button.grid(row=1, column=0,pady=5)
        self.run_number_label.grid(row=0, column=1)
        self.entry_box.grid(row=1, column=1)
        self.run_data_button.grid(row=2, column=0)
        self.min_files_entry.grid(row=2, column=1)
        self.tab1_layout.pack(pady=20)
        self.tab2_text.pack()
        self.tab1.pack()
        self.tab2.pack()

        # Zishaan attempt at placeholder text
        # Entry only accepts int I think
        # self.entry_box.insert(0, "Input run number here...")
        # self.entry_box.bind("<Button-1>", self.on_entry_click)

        self.notebook.add(self.tab1, text='Data Retrieval')
        self.notebook.add(self.tab2, text='Window2')

        self.title.pack()
        self.notebook.pack(expand=True, fill=BOTH)
        self.message_box.pack(anchor=W, side=TOP)

        def button_enabler(event):
            if len(self.entry_box.get()) >= 1:
                self.get_data_button.configure(state=NORMAL)
            else:
                self.get_data_button.configure(state=DISABLED)
                # Zishaan Addition
                self.run_data_button.configure(state=DISABLED)

        self.master.bind("<KeyRelease>", button_enabler)
    def int_checker(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def get_data(self):
        run_number = self.entry_box.get()
        if int(run_number) > 0:
            # Zishaan addition
            # min_files = str(self.min_files_entry.get())

            self.message_box_text.set('Data was definitely retrieved from run number ' +
            str(run_number) + '.')
            # Zishaan addition


            self.run_data_button.configure(state=NORMAL)
        else:
            self.message_box_text.set('Input a run number greater than 0.')

    def run_data(self):
        run_number = self.entry_box.get()
        self.message_box_text.set('Data from run number ' + str(run_number) + ' was definitely graphed.')


root = Tk()
Controller_GUI = Controller(root)
root.mainloop()