import sys
sys.path.extend([".",".."])

TICKER = 100
from lightk import base, ui, themes
top = base.Window("escapable","centralized", resizable=True)
ca = base.tk.Canvas(top,highlightthickness=0,bg="white")
base.default_pack(ca)

menu_group = ui.MenuGroup(ca,20,20,width=600,height=250)

entry_label = ui.Text(ca,20,280,text="Insert button's label:",anchor="nw")
entry = ui.tkEntry(ca,20,300,anchor="nw",width=600,height=40,theme=themes.LIGHT_ENTRY)
entry.widget.focus_force()
radius_label = ui.Text(ca,20,360,text="Radius",anchor="nw")

def _increase_radius(*evts):
	menu_group.radius = [i+1 for i in menu_group.radius]
	menu_group.update()
def _decrease_radius(*evts):
	if menu_group.radius[0] > 0:
		menu_group.radius = [i-1 for i in menu_group.radius]
		menu_group.update()

increase_radius_btn = ui.Button(ca,70,350,width=30,height=30,text="+")
increase_radius_btn.bind("<1>", _increase_radius, "+")
decrease_radius_btn = ui.Button(ca,102,350,width=30,height=30,text="-")
decrease_radius_btn.bind("<1>", _decrease_radius, "+")

def _press_return(*evts):
	_text = entry.widget.get()
	entry.widget.delete("0", base.tk.END)
	if _text:
		menu_group.add_command(text=_text)
entry.widget.bind("<Return>", _press_return, "+")

def _update_widgets(*evts):
	entry.update()
	entry_label.update()
	radius_label.update()
	menu_group.update()
	increase_radius_btn.update()
	decrease_radius_btn.update()
top.bind("<Configure>",_update_widgets,"+")

top.mainloop()