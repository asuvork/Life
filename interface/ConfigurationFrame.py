from tkinter import LabelFrame, BooleanVar, Checkbutton, IntVar, Spinbox, Scale, Frame, Button, Label
from tkinter import LEFT, TOP, DISABLED, Y, NW


class ConfigurationFrame:
    default_survive = [0, 0, 1, 1, 0, 0, 0, 0, 0]
    default_mask = [1, 1, 1, 1, 1, 1, 1, 1]
    default_born = 3
    default_width = 10
    default_height = 10

    class FieldOptions:
        def __init__(self, master, width, height):
            self.frame = LabelFrame(master, text="Field option")
            self.width = IntVar(value=width)
            self.height = IntVar(value=height)
            label_x = Label(self.frame, text="X: ")
            label_x.pack(side=LEFT)
            self.spin_box_width = Spinbox(self.frame, text="width", textvariable=self.width, wrap=True,
                                          to=2000, from_=10)
            self.spin_box_width.pack(side=LEFT, fill="x", expand=True)
            label_y = Label(self.frame, text="Y: ")
            label_y.pack(side=LEFT)
            self.spin_box_height = Spinbox(self.frame, text="height", textvariable=self.height, wrap=True,
                                           to=2000, from_=10)
            self.spin_box_height.pack(side=LEFT, fill="x", expand=True)
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

            self.frame.pack(side=LEFT)

        def get_values(self):
            return [cb.value.get() for cb in self.check_boxes]

    class BirthOptions:
        def __init__(self, master, count, default):
            self.frame = LabelFrame(master, text="Born option")
            self.value = IntVar(value=default)
            self.spin_box = Spinbox(self.frame, textvariable=self.value, wrap=True, width=int(count / 10 + 2),
                                    to=count - 1, from_=1)
            self.spin_box.pack(side=LEFT)
            self.scale = Scale(self.frame, variable=self.value, orient='horizontal', to=count - 1, from_=1, showvalue=0)
            self.scale.pack(side=LEFT, fill="x", expand=True)
            self.frame.pack(side=TOP, fill="x", expand=True)

        def get_values(self):
            return self.value.get()

    def __init__(self):
        self.frame = Frame()
        self.frame.pack(side=LEFT, fill='none', expand=False, anchor=NW)
        self.field_options = self.FieldOptions(self.frame, self.default_width, self.default_height)
        self.survive_options = self.SurviveOptions(self.frame, self.default_survive)
        self.birth_options = self.BirthOptions(self.frame, len(self.default_survive), self.default_born)
        self.mask_options = self.NeighboursOptions(self.frame, self.default_mask)
        self.commit_button = Button(self.frame, text='Commit')
        self.commit_button.pack(side=TOP, fill="x", expand=True)
        self.step_button = Button(self.frame, text='Step')
        self.step_button.pack(side=TOP, fill="x", expand=True)

    def get_rules(self):
        return {
            "mask": self.mask_options.get_values(),
            "survival_rule": self.survive_options.get_values(),
            "birth_rule": self.birth_options.get_values(),
        }

    def get_field_size(self):
        return self.field_options.get_values()


class CheckBox:
    def __init__(self, master, value, title=None):
        self.value = BooleanVar()
        self.value.set(value)
        self.title = title
        self.cb = Checkbutton(master, variable=self.value, onvalue=1, offvalue=0)
        if title is not None:
            self.cb.config(text=title)
