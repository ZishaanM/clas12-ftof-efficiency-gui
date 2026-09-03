from tkinter import *
from tkinter.ttk import *

class Controller:
    def __init__(self, master):
        self.master = master
        master.geometry('700x500')


        self.label = Label(master, text='Controller GUI')
        self.notebook = Notebook(master, padding=[30, 30, 30, 30])

        tab1 = Frame(self.notebook)
        tab1_layout = Frame(tab1)
        vcmd = master.register(self.int_checker)
        run_number_label = Label(tab1_layout, text = "Type Run Number Below")
        global entry_box
        entry_box = Entry(tab1_layout, validate='all', validatecommand=(vcmd, '%P'))
        global get_data_button
        get_data_button = Button(tab1_layout, text = "Retrieve Data From Run Number", state = DISABLED,
                                     command = self.retrieve_data)

        tab2 = Frame(self.notebook)
        tab2_text = Label(tab2, text='test2')

        get_data_button.grid(row=1, column=0, padx=10)
        run_number_label.grid(row=0, column=1)
        entry_box.grid(row=1, column=1)
        tab1_layout.place(x=60, y=25)
        tab2_text.pack()
        tab1.pack()
        tab2.pack()

        self.notebook.add(tab1, text = 'Data Retrieval')
        self.notebook.add(tab2, text='Window2')

        self.label.pack()
        self.notebook.pack(expand=True, fill=BOTH)

    def int_checker(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def retrieve_data(self):
        run_number = entry_box.get()
        print('Data was definitely retrieved from run number ' + str(run_number) + '.')

def button_enabler(event):
    if len(entry_box.get()) >= 1:
        get_data_button.configure(state=NORMAL)



root = Tk()
root.bind("<KeyRelease>", button_enabler)
Controller_GUI = Controller(root)
root.mainloop()