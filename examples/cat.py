#!/usr/bin/env python
import sys
sys.path.extend([".","..","../.."])
from lightk import base, game
top = base.Window("escapable","fullscreen")
ca = base.tk.Canvas(top,bg="white",highlightthickness=0)
base.default_pack(ca)

log = base.Label(ca,10,10,anchor="nw",text="Loading...",fill="#999",
	font=("TkDefaultFont",13,"bold"))
log.update(idle=True)

sprites = {
	"default" : [
		base.get_image("cat/c1.png"),
		base.get_image("cat/c2.png"),
		base.get_image("cat/c3.png"),
		base.get_image("cat/c4.png"),
		base.get_image("cat/c5.png"),
		base.get_image("cat/c6.png"),
		base.get_image("cat/c7.png"),
		base.get_image("cat/c8.png"),
		base.get_image("cat/c9.png"),
		base.get_image("cat/c10.png"),
		base.get_image("cat/c11.png"),
		base.get_image("cat/c12.png"),
	],
	"staying" : [
		base.get_image("cat/b1.png"),
		base.get_image("cat/b2.png"),
		base.get_image("cat/b3.png"),
		base.get_image("cat/b4.png"),
		base.get_image("cat/b5.png"),
		base.get_image("cat/b6.png"),
	],
	"run1" : [
		base.get_image("cat/a1.png"),
		base.get_image("cat/a2.png"),
		base.get_image("cat/a3.png"),
		base.get_image("cat/a4.png"),
		base.get_image("cat/a5.png"),
		base.get_image("cat/a6.png"),
		base.get_image("cat/a7.png"),
		base.get_image("cat/a8.png"),
		base.get_image("cat/a9.png"),
		base.get_image("cat/a10.png"),
		base.get_image("cat/a11.png"),
		base.get_image("cat/a12.png"),
	],
	"run2" : [
		base.get_image("cat/d1.png"),
		base.get_image("cat/d2.png"),
		base.get_image("cat/d3.png"),
		base.get_image("cat/d4.png"),
		base.get_image("cat/d5.png"),
		base.get_image("cat/d6.png"),
		base.get_image("cat/d7.png"),
		base.get_image("cat/d8.png"),
		base.get_image("cat/d9.png"),
		base.get_image("cat/d10.png"),
		base.get_image("cat/d11.png"),
		base.get_image("cat/d12.png"),
		base.get_image("cat/d13.png"),
	]
}
log.style.update(text="lk")
log.update(idle=True)

CAT = game.Sprite(ca, top.get_width()/2,
	top.get_height()/2, tk_photo=sprites["default"][0])
CAT.states = sprites
def _(*args):
	if top.kmap.get("Left",False):
		CAT.to_state("default")
		CAT.next()
	elif top.kmap.get("Right",False):
		CAT.to_state("run1")
		CAT.next()
	elif top.kmap.get("Up",False):
		CAT.to_state("run2")
		CAT.next()
	else:
		CAT.to_state("staying")
		if CAT.actual[1] != len(CAT.states["staying"]) - 1:
			CAT.next()
	CAT.update(idle=True, frames=True)
top.run(_,80)

top.mainloop()