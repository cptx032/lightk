#!/usr/bin/env python
import sys
sys.path.extend([".","..","../.."])

import Image, math
from lightk import base, game
top = base.Window("escapable","fullscreen")
ca = base.tk.Canvas(top, bg="white",highlightthickness=0)
base.default_pack(ca)

r_ = base.get_image("road.jpg")
road = base.Image(ca,top.get_width(), top.get_height(),
	anchor="se",tk_photo=r_.zoom(2))

main_car = game.Sprite(ca, top.get_width()/2,
	top.get_height()/2+100, tk_photo=base.get_image("car.png"))
main_car.angle = 0.0
main_car.increment = 10 # how many pixels the car 'run'
main_car.states["default"] = game.create_rot_level(Image.open("car.png"))
main_car.update(frames=True,idle=True)

def _run(*evts):
	# :clean
	if main_car.angle < -359:
		main_car.angle = -359 # inverted list index (ex: [a,b,c][-1] == c)
	if main_car.angle > 359:
		main_car.angle = 0

	if top.kmap.get("Up",False):
		# you can turn left|right only if you are running
		if top.kmap.get("Left",False):
			main_car.angle += 1.8
			main_car.to_frame(int(main_car.angle))
		if top.kmap.get("Right",False):
			main_car.angle -= 1.8
			main_car.to_frame(int(main_car.angle))
		# calculating angle
		y_increment = math.cos(math.radians(main_car.angle)) * main_car.increment
		x_increment = math.sin(math.radians(main_car.angle)) * main_car.increment
		road.coords[0] += x_increment
		road.coords[1] += y_increment
	road.update()
	main_car.update(frames=True,idle=True)
top.run(_run, 10)

top.mainloop()