from interface import commit_button, step_button, canvas, scale, config_frame, root
from models.Rules import Rules
from models.fields.BorderedField import BorderedField


class Life:
    def __init__(self):
        canvas.canvas.bind("<Button-1>", self.click)
        step_button.config(command=self.step)
        commit_button.config(command=self.commit)
        self.field = None
        root.mainloop()

    def commit(self):
        width, height = config_frame.get_field_size()
        rules = Rules(**config_frame.get_rules())
        self.field = BorderedField(width, height, rules)
        canvas.draw_grid(width, height)
        canvas.update_field(self.field.get_field())

    def click(self, event):
        if self.field:
            i = int(event.x / scale)
            j = int(event.y / scale)
            # print("clicked at - ", event.x, event.y, ", field - ", i, "---", j)
            # print(self.canvas.winfo_width(), self.canvas.winfo_height())
            value = self.field.inverse_point(i, j)
            canvas.update_cell(i, j, value)

    def step(self):
        if self.field:
            self.field.step()
            canvas.update_field(self.field.get_field())


if __name__ == '__main__':
    Life()
