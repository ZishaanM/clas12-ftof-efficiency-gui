import tkinter as tk

class MyGUI:
    def __init__(self):
        calc_ind = 0

        #root var = window
        self.root = tk.Tk()

        #sets the geometry of the window
        self.root.geometry("500x700")

        self.label = tk.Label(self.root, activebackground=("cyan"), text="Tkinter Calculator", font=("Algerian"))
        self.label.pack(pady=40)

        fontZ = "Calibri"

        self.textbox = tk.Text(self.root, height=1, font=(fontZ, 20))
        self.textbox.pack(fill='x')
        self.textbox.pack(padx=20, pady=50)

        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0, weight=4)
        self.buttonframe.columnconfigure(1, weight=4)
        self.buttonframe.columnconfigure(2, weight=4)
        self.buttonframe.columnconfigure(3, weight=4)

        btn1 = tk.Button(self.buttonframe, text="7", font=(fontZ, 18))
        btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
        if btn1:
            buttonClicked(7)

        btn2 = tk.Button(self.buttonframe, text="8", font=(fontZ, 18))
        btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

        btn3 = tk.Button(self.buttonframe, text="9", font=(fontZ, 18))
        btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

        btn4 = tk.Button(self.buttonframe, text="÷", font=(fontZ, 18))
        btn4.grid(row=0, column=3, sticky=tk.W+tk.E)

        btn5 = tk.Button(self.buttonframe, text="4", font=(fontZ, 18))
        btn5.grid(row=1, column=0, sticky=tk.W+tk.E)

        btn6 = tk.Button(self.buttonframe, text="5", font=(fontZ, 18))
        btn6.grid(row=1, column=1, sticky=tk.W+tk.E)

        btn7 = tk.Button(self.buttonframe, text="6", font=(fontZ, 18))
        btn7.grid(row=1, column=2, sticky=tk.W+tk.E)

        btn8 = tk.Button(self.buttonframe, text="x", font=(fontZ, 18))
        btn8.grid(row=1, column=3, sticky=tk.W+tk.E)

        btn9 = tk.Button(self.buttonframe, text="1", font=(fontZ, 18))
        btn9.grid(row=2, column=0, sticky=tk.W+tk.E)

        btn10 = tk.Button(self.buttonframe, text="2", font=(fontZ, 18))
        btn10.grid(row=2, column=1, sticky=tk.W+tk.E)

        btn11 = tk.Button(self.buttonframe, text="3", font=(fontZ, 18))
        btn11.grid(row=2, column=2, sticky=tk.W+tk.E)

        btn12 = tk.Button(self.buttonframe, text="-", font=(fontZ, 18))
        btn12.grid(row=2, column=3, sticky=tk.W+tk.E)

        btn13 = tk.Button(self.buttonframe, text=".", font=(fontZ, 18))
        btn13.grid(row=3, column=0, sticky=tk.W+tk.E)

        btn14 = tk.Button(self.buttonframe, text="0", font=(fontZ, 18))
        btn14.grid(row=3, column=1, sticky=tk.W+tk.E)

        btn15 = tk.Button(self.buttonframe, text="=", font=(fontZ, 18))
        btn15.grid(row=3, column=2, sticky=tk.W+tk.E)

        btn16 = tk.Button(self.buttonframe, text="+", font=(fontZ, 18))
        btn16.grid(row=3, column=3, sticky=tk.W+tk.E)

        self.buttonframe.pack(fill='x')

        self.root.mainloop()

        def buttonClicked(key):
            print(key)

        def calculate():
            num = 0

MyGUI()