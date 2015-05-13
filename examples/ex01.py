#!/usr/bin/env python
import sys
sys.path.extend([".",".."])
import base

top = base.Window("fullscreen","escapable")
ca = base.tk.Canvas(top,bg="black")
ca.config(bd=0,highlightthickness=0)
ca.pack(expand="yes",fill="both")

r = base.RoundedRectangle(ca,250,250,radius=[100,100,100,100],width=100,
	height=50,outline="red",fill="white")

def over(*args):
	r.style["fill"] = "red"
	r.style["outline"] = "white"

def leave(*args):
	r.style["fill"] = "white"
	r.style["outline"] = "red"

r.bind("<Motion>", over, "+")
r.bind("<Leave>", leave, "+")
# r.level = 100
def run(*args):
	r.radius = [i+1 for i in r.radius]
	r.update(idle=True)
base.Label(ca,1200,750,anchor="sw",text="Loading...",fill="white",font=("TkDefaultFont", 12,"bold"))
top.run(run, 24)
top.mainloop()