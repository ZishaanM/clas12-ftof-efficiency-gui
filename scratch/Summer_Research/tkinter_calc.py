import tkinter as tk

#root var = window
root = tk.Tk()

#sets the geometry of the window
root.geometry("500x700")

label = tk.Label(root, activebackground=("blue"), text="Tkinter Calculator", font=("Algerian"))
label.pack(pady=40)

fontZ = "Calibri"

answer = ""
ansBox = tk.Label(root, text=answer, height=3, width=20, font=(fontZ, 15), justify=tk.RIGHT)
ansBox.pack(anchor='e', padx=0, pady=0)

def shortcuts(event):
    
    if event.state == 8 and event.keysym == "Return":
        calculate()
    if event.state == 8 and event.keysym == "c":
        clear_text()
    if event.state == 9 and event.keysym == "C":
        ansBox.config(text="")
        clear_text()
    

entry = tk.Entry(root, width=16, font=(fontZ, 20), justify=tk.RIGHT)
entry.pack(fill='x')
entry.pack(padx=20, pady=50)
entry.bind("<KeyPress>", shortcuts)
entry.bind("<KeyPress>", shortcuts)

# checkbox = tk.Checkbutton(root, text="Keep solution in box"
#                         , font=(fontZ, 18), variable = check_state)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=4)
buttonframe.columnconfigure(1, weight=4)
buttonframe.columnconfigure(2, weight=4)
buttonframe.columnconfigure(3, weight=4)

def buttonClicked(value):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + value)

def calculate():
    try:
        # Solves problem and stores in variable
        ans = eval(entry.get())
        print(ans)
        #Deletes problem from the input box
        entry.delete(0, tk.END)
        #if use_prev_soln == True:
        entry.insert(0, str(ans))
        print(ansBox.cget("text"))
        store = ansBox.cget("text")
        ansBox.config(text=str(store) + '\n' + str(ans))
    except:
        ansBox.config(text="Error")


def clear_text():
    entry.delete(0, tk.END)


btn1 = tk.Button(buttonframe, text="7", font=(fontZ, 18), command=lambda: buttonClicked("7"))
btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

btn2 = tk.Button(buttonframe, text="8", font=(fontZ, 18), command=lambda: buttonClicked("8"))
btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

btn3 = tk.Button(buttonframe, text="9", font=(fontZ, 18), command=lambda: buttonClicked("9"))
btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

btn4 = tk.Button(buttonframe, text="÷", font=(fontZ, 18), command=lambda: buttonClicked("/"))
btn4.grid(row=0, column=3, sticky=tk.W+tk.E)

btn5 = tk.Button(buttonframe, text="4", font=(fontZ, 18), command=lambda: buttonClicked("4"))
btn5.grid(row=1, column=0, sticky=tk.W+tk.E)

btn6 = tk.Button(buttonframe, text="5", font=(fontZ, 18), command=lambda: buttonClicked("5"))
btn6.grid(row=1, column=1, sticky=tk.W+tk.E)

btn7 = tk.Button(buttonframe, text="6", font=(fontZ, 18), command=lambda: buttonClicked("6"))
btn7.grid(row=1, column=2, sticky=tk.W+tk.E)

btn8 = tk.Button(buttonframe, text="x", font=(fontZ, 18), command=lambda: buttonClicked("*"))
btn8.grid(row=1, column=3, sticky=tk.W+tk.E)

btn9 = tk.Button(buttonframe, text="1", font=(fontZ, 18), command=lambda: buttonClicked("1"))
btn9.grid(row=2, column=0, sticky=tk.W+tk.E)

btn10 = tk.Button(buttonframe, text="2", font=(fontZ, 18), command=lambda: buttonClicked("2"))
btn10.grid(row=2, column=1, sticky=tk.W+tk.E)

btn11 = tk.Button(buttonframe, text="3", font=(fontZ, 18), command=lambda: buttonClicked("3"))
btn11.grid(row=2, column=2, sticky=tk.W+tk.E)

btn12 = tk.Button(buttonframe, text="-", font=(fontZ, 18), command=lambda: buttonClicked("-"))
btn12.grid(row=2, column=3, sticky=tk.W+tk.E)

btn13 = tk.Button(buttonframe, text=".", font=(fontZ, 18), command=lambda: buttonClicked("."))
btn13.grid(row=3, column=0, sticky=tk.W+tk.E)

btn14 = tk.Button(buttonframe, text="0", font=(fontZ, 18), command=lambda: buttonClicked("0"))
btn14.grid(row=3, column=1, sticky=tk.W+tk.E)

btn15 = tk.Button(buttonframe, text="=", font=(fontZ, 18), command=calculate)
btn15.grid(row=3, column=2, sticky=tk.W+tk.E)

btn16 = tk.Button(buttonframe, text="+", font=(fontZ, 18), command=lambda: buttonClicked("+"))
btn16.grid(row=3, column=3, sticky=tk.W+tk.E)

buttonframe.pack(fill='x')

clear = tk.Button(root, text="Clear (c, C)", font=(fontZ, 12), command=clear_text)
clear.pack(padx=110, pady=20)


root.mainloop()