from tkinter import Tk
from interface.ConfigurationFrame import ConfigurationFrame
from interface.FieldFrame import FieldFrame


root = Tk()
root.title("Life")

config_frame = ConfigurationFrame()
field_frame = FieldFrame()

commit_button = config_frame.commit_button
step_button = config_frame.step_button
randomize_button = config_frame.randomize.randomize_button
canvas = field_frame.field_canvas
scale = field_frame.default_scale
