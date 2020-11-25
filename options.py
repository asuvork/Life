from tkinter import Tk, Entry, Button, Label

class SurviveOptions:
    def __init__(self, master):
        self.var = BooleanVar()
        self.var.set(0)
        self.cb = Checkbutton(master, text=title, variable=self.var, onvalue=True, offvalue=0)
        self.cb.pack(side=LEFT)