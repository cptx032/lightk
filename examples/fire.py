#!/usr/bin/env python
from lightk import base
import random

top = base.Window(title="Fire")
top.fullscreen()
base.enable_escape(top)
ca = base.tk.Canvas(top, bg="#2a2a2a", highlightthickness=0)
ca.pack(expand="yes", fill="both")

class Circle(object):
	def __init__(self, ca, *xy, **kws):
		self.xy = list(xy)
		self.radius = kws.pop("radius", 10)
		self.kws = kws
		self.canvas = ca
		self.index = self.draw()
	def draw(self):
		return self.canvas.create_oval(self.xy[0]-self.radius,
			self.xy[1]-self.radius, self.xy[0]+self.radius,
			self.xy[1]+self.radius, **self.kws)
	def update(self):
		self.coords = [
			self.xy[0] - self.radius,
			self.xy[1] - self.radius,
			self.xy[0] + self.radius,
			self.xy[1] + self.radius
		]
		if self.index:
			self.canvas.itemconfig(self.index, **self.kws)
			self.canvas.coords(self.index, *self.coords)

STAGES = [
	{"fill":"#f77", "outline":"#f77"},
	{"fill":"darkorange", "outline":"darkorange"},
	{"fill":"red", "outline":"red"}
]
# STAGES = [
# 	{"fill":"#8a8a8a", "outline":"#8a8a8a"},
# 	{"fill":"darkgray", "outline":"darkgray"},
# 	{"fill":"lightgray", "outline":"lightgray"}
# ]
RADIUS = 0.1
class Particle(Circle):
	LIFE_TIME = 100
	TICKER = 10
	GRAVITY = -.018
	def __init__(self, ca, *xy, **kws):
		self.vel = kws.pop("vel", [0,0])
		self.life = Particle.LIFE_TIME
		Circle.__init__(self, ca, *xy, **kws)
		self.process()
	def process(self):
		self.xy[0] += self.vel[0]
		self.xy[1] += self.vel[1]
		self.vel[1] += Particle.GRAVITY
		self.life -= 1
		self.radius = RADIUS

		# anim
		if self.life > 0 and self.life < 20:
			self.kws = STAGES[2]
		elif self.life > 20 and self.life < 50:
			self.kws = STAGES[1]
		elif self.life > 50 and self.life < 100:
			self.kws = STAGES[0]

		self.update()
		if self.life <= 0:
			self.canvas.delete(self.index)
			self.index = None
		if self.index:
			self.canvas.after(Particle.TICKER, self.process)

def emit():
	x,y = top.get_relative_mouse_pos()
	for i in range(0, random.randint(1,2)):
		Particle(ca, x, y,vel=[random.randint(-1,1), random.randint(-4,1)])
	ca.after(30, emit)
emit()
def increase_radius(*args):
	global RADIUS
	RADIUS += 1
def decrease_radius(*args):
	global RADIUS
	RADIUS -= 1
def switch(*args):
	global STAGES
	if STAGES[0]["fill"] == "#f77":
		STAGES = [
			{"fill":"#8a8a8a", "outline":"#8a8a8a"},
			{"fill":"darkgray", "outline":"darkgray"},
			{"fill":"lightgray", "outline":"lightgray"}
		]
	else:
		STAGES = [
			{"fill":"#f77", "outline":"#f77"},
			{"fill":"darkorange", "outline":"darkorange"},
			{"fill":"red", "outline":"red"}
		]

top.bind("<Right>", increase_radius, "+")
top.bind("<Left>", decrease_radius, "+")
top.bind("<s>", switch, "+")
top["cursor"] = "none"
top.mainloop()