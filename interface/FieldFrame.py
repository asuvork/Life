from tkinter import Canvas, Scrollbar, Button, LEFT, BOTH, Frame
from tkinter import HORIZONTAL, VERTICAL, X, BOTTOM, RIGHT, Y


class FieldFrame:
    default_scale = 10

    class FieldCanvas:
        def __init__(self, master, scale):
            self.scale = scale
            self.cells = None
            self.height = None
            self.width = None
            # self.canvas = Canvas(master, bg='white', borderwidth=0, highlightthickness=0)
            self.canvas = Canvas(master, bg='white', bd=0, highlightthickness=0, width=0, height=0)
            self.h_bar = Scrollbar(master, orient=HORIZONTAL)
            self.v_bar = Scrollbar(master, orient=VERTICAL)
            self.h_bar.pack(side=BOTTOM, fill=X)
            self.h_bar.config(command=self.canvas.xview)
            self.v_bar.pack(side=RIGHT, fill=Y)
            self.v_bar.config(command=self.canvas.yview)
            self.canvas.config(xscrollcommand=self.h_bar.set, yscrollcommand=self.v_bar.set)

            self.canvas.bind("<MouseWheel>", self._scroll_vertical)
            self.canvas.bind('<Shift-MouseWheel>', self._scroll_horizontal)
            self.canvas.pack(fill="none", expand=True)

        def _scroll_vertical(self, event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _scroll_horizontal(self, event):
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        def draw_grid(self, width, height):
            self.cells = []
            self.canvas.delete("all")
            self.width = width
            self.height = height
            scaled_width = width * self.scale
            scaled_height = height * self.scale
            self.canvas.config(width=scaled_width, height=scaled_height,
                               scrollregion=(0, 0, scaled_width, scaled_height))
            for j in range(height):
                self.cells.append([])
                for i in range(width):
                    x = i * self.scale
                    y = j * self.scale
                    self.cells[j].append(
                        self.canvas.create_rectangle(x, y, x + self.scale, y + self.scale, fill='white'))

        def update_field(self, field_array):
            # print(field_array)
            for j in range(self.height):
                for i in range(self.width):
                    # print(j, i)
                    value = field_array[j][i]
                    self.update_cell(i, j, value)

        def update_cell(self, i, j, value):
            if value:
                self.canvas.itemconfig(self.cells[j][i], fill='black')
            else:
                self.canvas.itemconfig(self.cells[j][i], fill='white')

    def __init__(self):
        self.frame = Frame()
        self.frame.pack(side=LEFT, expand=True, fill=BOTH)
        self.field_canvas = self.FieldCanvas(self.frame, self.default_scale)
