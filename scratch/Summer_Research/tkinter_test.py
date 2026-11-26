import tkinter as tk

#creates GUI window
root = tk.Tk()
root.title("Tkinter Example")

label = tk.Label(root, text="Hello, Tkinter!")
label.pack()

button = tk.Button(root, text="Click Me", command=lambda: print("Button clicked"))
button.pack()

root.mainloop()
