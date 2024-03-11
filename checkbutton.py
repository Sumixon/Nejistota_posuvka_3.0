from tkinter import *
from tkinter import ttk
import tkinter as tk

def checkbutton_clicked():


    print("Newstate: ", checkbutton_value.get())


root = Tk()
root.title("Checkbutton in Tk")
root.minsize(500, 200)
checkbutton_value = tk.BooleanVar()
checkbutton = ttk.Checkbutton(

    text="Doplníme do programu pro upřesnění výpočtu",

    variable=checkbutton_value,

    command=checkbutton_clicked
)
checkbutton.place(x=40,
                  y=70)
root.mainloop()