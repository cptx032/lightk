#!/usr/bin/env python
import sys
sys.path.extend(['.','..','../..'])
from lightk import base, ui, themes as Themes
top = base.Window(title="Sprint simulation")
top.fullscreen()
base.enable_escape(top)
ca = base.tk.Canvas(top,highlightthickness=0,bg="#2a2a2a")
ca.pack(expand="yes",fill="both")
Themes.DARK_ENTRY["over"]["bg"] = "#454545"

class Body(base.Rectangle):
	TICKER = 10
	def __init__(self, *args,**kws):
		self.vel = kws.pop("vel",[0,0])
		self.acel = kws.pop("acel",[0,0])
		base.Rectangle.__init__(self,*args,**kws)
		self.style = Themes.DARK_BTN[1]["over"]
		self.update()
		self.process()
	def process(self):
		self.coords[0] += self.vel[0]
		self.coords[1] += self.vel[1]
		self.vel[0] += self.acel[0]
		self.vel[1] += self.acel[1]
		if self.index:
			self.canvas.after(Body.TICKER, self.process)
		self.update()

SPRING_SIZE = 280 # REST POSITION
SPRING_K = 0.01
DAMPING = 0.92
BODY_MASS = 0.8

b1 = Body(ca,20,SPRING_SIZE,width=100,height=100)
spring = base.Line(ca, b1.coords[0]+b1.width/2,0,b1.coords[0]+b1.width/2,SPRING_SIZE,fill="#ddd")

def run(*args):
	F = -SPRING_K * (b1.coords[1]-SPRING_SIZE)
	b1.acel[1] = F / BODY_MASS
	b1.vel[1] *= DAMPING
	spring.coords = [b1.coords[0]+b1.width/2,0,b1.coords[0]+b1.width/2,b1.coords[1]]
	spring.update()
top.run(run, Body.TICKER)

def set_b_pos(evt):
	b1.coords[1] = evt.y
ca.bind("<1>", set_b_pos,"+")

# User Interface
ui.Text(ca,350,50,text="Mass",fill="#888",no_shadow=1)
ui.Text(ca,340,100,text="Damping",fill="#888",no_shadow=1)
ui.Text(ca,340,150,text="Spring K",fill="#888",no_shadow=1)
ui.Text(ca,325,200,text="Update Ticker",fill="#888",no_shadow=1)

mass_field = ui.tkEntry(ca,420,50,width=200,height=40,theme=Themes.DARK_ENTRY,anchor="w")
mass_field.widget.configure(justify="right",foreground="#888",bg="#3a3a3a",highlightthickness=0)

D_field = ui.tkEntry(ca,420,100,width=200,height=40,theme=Themes.DARK_ENTRY,anchor="w")
D_field.widget.configure(justify="right",foreground="#888",bg="#3a3a3a",highlightthickness=0)

K_field = ui.tkEntry(ca,420,150,width=200,height=40,theme=Themes.DARK_ENTRY,anchor="w")
K_field.widget.configure(justify="right",foreground="#888",bg="#3a3a3a",highlightthickness=0)

T_field = ui.tkEntry(ca,420,200,width=200,height=40,theme=Themes.DARK_ENTRY,anchor="w")
T_field.widget.configure(justify="right",foreground="#888",bg="#3a3a3a",highlightthickness=0)

# initing values
mass_field.widget.insert(0, str(BODY_MASS))
D_field.widget.insert(0, str(DAMPING))
K_field.widget.insert(0,str(SPRING_K))
T_field.widget.insert(0,str(Body.TICKER))

update_btn = ui.Button(ca,280,250,theme=Themes.DARK_BTN,width=350,height=50,text="Update",no_shadow=1)

def _update(*args):
	global BODY_MASS, DAMPING, SPRING_K
	BODY_MASS = float(mass_field.text.get())
	DAMPING = float(D_field.text.get())
	SPRING_K = float(K_field.text.get())
	Body.TICKER = int(T_field.text.get())
update_btn.bind("<ButtonRelease-3>",_update,"+")

top.mainloop()
