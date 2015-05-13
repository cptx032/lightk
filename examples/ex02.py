#!/usr/bin/env python
import sys
sys.path.extend([".","..",])

import base, game, ui
top = base.Window("centralized", "escapable", title="UI Test", resizable=True)
ca = base.tk.Canvas(top, highlightthickness=0,bg="white")
base.default_pack(ca)

btn1 = ui.Button(ca,50,50,
	theme=ui.themes.LIGHT_BTN,
	width=100,height=100,text="OK")

v_scroll = ui.Scrollbar(ca,310,300,width=6,height=100)
v_scroll.style = ui.themes.LIGHT_BTN[1]["normal"]
v_scroll.update()
v_scroll.bar.theme = ui.themes.DARK_BTN
v_scroll.bar._release()

l_widget = ui.uiFrame(ca,0,0,anchor="nw",width=300,height=100)
l = base.tk.Listbox(l_widget.frame)
l_widget.pack_widget(l)
for i in range(50):
	l.insert(base.tk.END,i)

l.config(yscrollcommand=v_scroll.set)
v_scroll.command = l.yview

def _(*args):
	btn1.update()
	v_scroll.update()
	l_widget.update()
# ca.bind("<Configure>", _, "+")
top.run(_, 1)
top.mainloop()
