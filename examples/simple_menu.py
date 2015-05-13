#!/usr/bin/env python
import sys
sys.path.extend(["./","../","../.."])
from lightk import base, ui
top = base.Window("centralized","escapable",resizable=True)
ca = base.tk.Canvas(top,bg="#fff",highlightthickness=0)
base.default_pack(ca)

menu_g = ui.MenuGroup(ca,2,2,width=640-4,height=400,theme=ui.themes.LIGHT_BTN,
	radius=[10,10,10,10],pady=5,padx=5)
def _to_vertical(*args):
	menu_g.orient = base.tk.VERTICAL
	menu_g.update()
def _to_horizontal(*args):
	menu_g.orient = base.tk.HORIZONTAL
	menu_g.update()
menu_g.add_command(text="Orient Vertical",no_shadow=0)
menu_g.commands[-1].bind("<1>", _to_vertical, "+")
menu_g.add_command(text="Orient Horizontal",no_shadow=0)
menu_g.commands[-1].bind("<1>",_to_horizontal,"+")

menu_g.add_command(text="File",no_shadow=0)
menu_g.add_command(text="Edit",no_shadow=0)
menu_g.add_command(text="Selection",no_shadow=0)
label = ui.Text(ca,640/2,450,text="Resize the window")

def _update(*args):
	label.update()
	menu_g.update(idle=True)
top.bind("<Configure>",_update,"+")
top.mainloop()