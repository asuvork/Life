from tkinter import BooleanVar, Checkbutton, LEFT, Frame, TOP, Tk, LabelFrame, Scale, Spinbox, IntVar, Y, DISABLED, \
    Canvas, Button, Scrollbar, VERTICAL, BOTTOM, HORIZONTAL, X, RIGHT, BOTH

from fields import BorderedField
from rules import Rules


class Interface:
    default_survive = [0, 0, 1, 1, 0, 0, 0, 0, 0]
    default_mask = [1, 1, 1, 1, 1, 1, 1, 1]
    default_born = 3
    default_width = 10
    default_height = 10
    default_scale = 20

    def __init__(self):
        root = Tk()
        self.parameters_frame = Frame()
        self.field_options = FieldOptions(self.parameters_frame, Interface.default_width, Interface.default_height)
        self.survive_options = SurviveOptions(self.parameters_frame, Interface.default_survive)
        self.born_options = BornOptions(self.parameters_frame, len(Interface.default_survive), Interface.default_born)
        self.mask_options = NeighboursOptions(self.parameters_frame, Interface.default_mask)
        self.commit_button = Button(self.parameters_frame, text='Commit', command=self.commit)
        self.commit_button.pack()
        self.parameters_frame.pack(side=LEFT, fill=Y)

        self.canvas_frame = Frame()
        self.field = None
        self.canvas_frame.pack(side=LEFT, expand=True, fill=BOTH)

        root.mainloop()

    def commit(self):
        width, height = self.field_options.get_values()
        rules = Rules(self.mask_options.get_values(), self.survive_options.get_values(), self.born_options.get_values())
        field = BorderedField(width, height, rules)
        if self.field is None:
            self.field = Field(self.canvas_frame, field, Interface.default_scale)
        else:
            self.field.update(field, Interface.default_scale)


class Field:
    def __init__(self, master, field: BorderedField, scale):
        self.field = None
        self.scale = None
        self.cells = None
        # self.canvas = Canvas(master, bg='white', borderwidth=0, highlightthickness=0)
        self.canvas = Canvas(master, bg='white', bd=0, highlightthickness=0)
        self.canvas.bind("<Button-1>", self.click)

        self.h_bar = Scrollbar(master, orient=HORIZONTAL)
        self.v_bar = Scrollbar(master, orient=VERTICAL)
        self.h_bar.pack(side=BOTTOM, fill=X)
        self.h_bar.config(command=self.canvas.xview)
        self.v_bar.pack(side=RIGHT, fill=Y)
        self.v_bar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=self.h_bar.set, yscrollcommand=self.v_bar.set)
        self.canvas.pack()
        self.step_button = Button(master, text='Step', command=self.step)
        self.step_button.pack()
        self.update(field, scale)

    def update(self, field: BorderedField, scale):
        self.field = field
        self.scale = scale
        self.cells = []
        self.canvas.delete("all")
        self.canvas.config(width=field.width*scale, height=field.height*scale, scrollregion=(0, 0, field.width*scale, field.height*scale))
        for j in range(self.field.height):
            self.cells.append([])
            for i in range(self.field.width):
                x = i * self.scale
                y = j * self.scale
                self.cells[j].append(self.canvas.create_rectangle(x, y, x + self.scale, y + self.scale, fill='white'))

    def draw(self):
        for j in range(self.field.height):
            for i in range(self.field.width):
                value = self.field.get_point(i, j)
                if value:
                    self.canvas.itemconfig(self.cells[j][i], fill='black')
                else:
                    self.canvas.itemconfig(self.cells[j][i], fill='white')

    def click(self, event):
        i = int(event.x / self.scale)
        j = int(event.y / self.scale)
        # print("clicked at - ", event.x, event.y, ", field - ", i, "---", j)
        # print(self.canvas.winfo_width(), self.canvas.winfo_height())
        value = self.field.inverse_point(i, j)
        if value:
            self.canvas.itemconfig(self.cells[j][i], fill='black')
        else:
            self.canvas.itemconfig(self.cells[j][i], fill='white')
        # self.field.print()

    def step(self):
        # self.field.print()
        self.field.step()
        self.draw()


class FieldOptions:
    def __init__(self, master, width, height):
        self.frame = LabelFrame(master, text="Field option")
        self.width = IntVar(value=width)
        self.height = IntVar(value=height)
        self.spin_box_width = Spinbox(self.frame, text="width", textvariable=self.width, wrap=True,
                                      to=2000, from_=10)
        self.spin_box_width.pack(side=LEFT)
        self.spin_box_height = Spinbox(self.frame, text="height", textvariable=self.height, wrap=True,
                                       to=2000, from_=10)
        self.spin_box_height.pack(side=LEFT)
        self.frame.pack(side=TOP, fill="x", expand=True)

    def get_values(self):
        return self.width.get(), self.height.get()


class SurviveOptions:
    def __init__(self, master, default):
        count = len(default)
        self.frame = LabelFrame(master, text="Survive option")
        self.check_boxes = []
        for i in range(count):
            check_box = CheckBox(self.frame, default[i], str(i))
            self.check_boxes.append(check_box)
            check_box.cb.pack(side=LEFT)
        self.frame.pack(side=TOP, fill="x", expand=True)

    def get_values(self):
        return [cb.value.get() for cb in self.check_boxes]


class NeighboursOptions:
    def __init__(self, master, default):
        self.frame = LabelFrame(master, text="Neighbour option")
        self.check_boxes = []

        for i in range(3):
            check_box = CheckBox(self.frame, default[i])
            self.check_boxes.append(check_box)
            check_box.cb.grid(row=0, column=i)
        check_box = CheckBox(self.frame, default[3])
        self.check_boxes.append(check_box)
        check_box.cb.grid(row=1, column=0)
        check_box = CheckBox(self.frame, 0)
        check_box.cb['state'] = DISABLED
        check_box.cb.grid(row=1, column=1)
        check_box = CheckBox(self.frame, default[4])
        self.check_boxes.append(check_box)
        check_box.cb.grid(row=1, column=2)
        for i in range(3):
            check_box = CheckBox(self.frame, default[i + 5])
            self.check_boxes.append(check_box)
            check_box.cb.grid(row=2, column=i)

        self.frame.pack(side=TOP, fill="x", expand=True)

    def get_values(self):
        return [cb.value.get() for cb in self.check_boxes]


class CheckBox:
    def __init__(self, master, value, title=None):
        self.value = BooleanVar()
        self.value.set(value)
        self.title = title
        if title is not None:
            self.cb = Checkbutton(master, text=title, variable=self.value, onvalue=1, offvalue=0)
        else:
            self.cb = Checkbutton(master,  variable=self.value, onvalue=1, offvalue=0)


class BornOptions:
    def __init__(self, master, count, default):
        self.frame = LabelFrame(master, text="Born option")
        self.value = IntVar(value=default)
        self.spin_box = Spinbox(self.frame, textvariable=self.value, wrap=True, width=int(count / 10 + 2),
                                to=count-1, from_=1)
        self.spin_box.pack(side=LEFT)
        self.scale = Scale(self.frame, variable=self.value, orient='horizontal', to=count-1, from_=1, showvalue=0)
        self.scale.pack(side=LEFT)
        self.frame.pack(side=TOP, fill="x", expand=True)

    def get_values(self):
        return self.value.get()
