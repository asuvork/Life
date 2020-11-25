from typing import List
from tkinter import Tk, Entry, Button, Label
from fields import BorderedField


class BooleanLife:
    def __init__(self) -> None:
        super().__init__()


if __name__ == '__main__':
    def str_to_sort_list(event):
        s = ent.get()
        s = s.split()
        s.sort()
        lab['text'] = ' '.join(s)

    root = Tk()
    ent = Entry(root, width=20)
    but = Button(root, text="Преобразовать")
    lab = Label(root, width=20, bg='black', fg='white')
    but.bind('<Button-1>', str_to_sort_list)
    ent.pack()
    but.pack()
    lab.pack()
    root.mainloop()
