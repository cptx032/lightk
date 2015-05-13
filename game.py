#!/usr/bin/env python
# Author: Willie Lawrence
"""
game description
"""
import base, ui
import ImageTk

def create_rot_level(pil_image,init=0,end=360,r_increase=1):
	"""
	This function returns a list with many PhotoImage instances
	each with the same image but rotated x angles.
	ARGS:
		pil_image: An instance of PIL.Image
		init: The init angle to rotation
		end: The final angle of rotation
		r_increase: The increase of degrees rotation
	init and end attributes are in degrees. The rotation is CCW
	(counterclockwise). The rotation attributes are integers.
	"""
	_result = list()
	for i in range(init, end, r_increase):
		_result.append( ImageTk.PhotoImage(pil_image.rotate(i)) )
	return _result
def create_alpha_level(pil_image,init=0,end=255,a_increase=1):
	"""
	This function returns a list with many PhotoImage instances
	each with the same image but with its alpha equal to x.
	ARGS:
		pil_image: An instance of PIL.Image
		init: The init alpha value
		end: The last alpha value
		a_increase: The increase of alpha variation
	The max value of alpha is 255 and minumum is 0 (zero).
	If you only call the function you will have a fadein
	effect (0 to 255 alpha value). If you want have a fadeout
	effect you should call the 'reverse' list method.
	"""
	_result = list()
	for i in range(init, end, a_increase):
		_img_copy = pil_image
		_img_copy.putalpha(i)
		_result.append( ImageTk.PhotoImage(_img_copy) )
	return _result

# FIXME
# def create_sprite_levels(pil_image, k_list, row, column, s_type="horizontal"):
# 	"""
# 		k_list: is a list with levels names
# 		row: how many rows has the sprite texture
# 		column: how many columns has the sprite texture
# 		s_type: horizontal | vertical
# 			The sprites are in [horizontal|vertical] order
# 	"""
# 	_result = dict()
# 	_width, _height = pil_image.size
# 	if s_type == "vertical":
# 		_col_counter = 0
# 		for x in range(0, _width, int(_width/column)):
# 			# print x, x+int(_width/column)
# 			_kname = k_list[_col_counter]
# 			_result[_kname] = []
# 			for y in range(0, _height, int(_height/row)):
# 				# y: vai de y ate y + int(_height/row)
# 				_tmp_img = pil_image.crop([x,y,x+int(_width/column),y+int(_height/row)])
# 				_result[_kname].append(ImageTk.PhotoImage(_tmp_img))
# 			_col_counter += 1
# 	elif s_type == "horizontal":
# 		_row_counter = 0
# 		for y in range(0, _height, int(_height/row)):
# 			_kname = k_list[_row_counter]
# 			_result[_kname] = []
# 			for x in range(0, _width, int(_width/column)):
# 				_tmp_img = pil_image.crop([x,y,x+int(_width/column),y+int(_height/row)])
# 				_ppp = ImageTk.PhotoImage(_tmp_img)
# 				_result[_kname].append(_ppp)
# 			_row_counter += 1
# 	return _result

class Sprite(base.Image):
	def __init__(self,*args,**kws):
		self.states = kws.pop("states", dict())
		self.actual = ["default",0]
		base.Image.__init__(self,*args,**kws)
		self.states["default"] = [self.tk_photo]
	def next(self):
		self.actual[1] += 1
		if self.actual[1] >= len(self.states[self.actual[0]]):
			self.actual[1] = 0 # return to begin
	def previous(self):
		self.actual[1] -= 1
		if self.actual[1] < 0:
			self.actual[1] = len(self.states[self.actual[0]]) - 1 # return to ultimate frame
	def to_state(self, state_name):
		self.actual[0] = state_name
	def to_frame(self, level_index):
		self.actual[1] = level_index
	def update(self, **kws):
		if kws.get("frames",False):
			self.tk_photo = self.states[self.actual[0]][self.actual[1]]
		base.Image.update(self)

class Body(base.BaseDraw):
	def __init__(self,*args,**kws):
		self.vel = kws.pop("vel",[0,0])
		self.accel = kws.pop("accel",[0,0])
		self.mass = kws.pop("mass", 1.0)
		self.obj = kws.pop("obj", None)
		base.BaseDraw.__init__(self,*args,**kws)
	def update_physics(self):
		self.coords[0] += self.vel[0]
		self.coords[1] += self.vel[1]
		self.vel[0] += self.accel[0]
		self.vel[1] += self.accel[1]
	def update(self, *args, **kws):
		# if kws.pop("physics", False):
		self.update_physics()
		if self.obj:
			self.obj.coords = self.coords
			self.obj.update()
		base.BaseDraw.update(self,*args,**kws)
	def apply_force(self, value):
		# F = ma; a = F / m
		self.accel[0] += float(value[0]) / self.mass
		self.accel[1] += float(value[1]) / self.mass

class Spring(Body):
	def __init__(self,*args,**kws):
		self.size = kws.pop("size") # spring rest position (x,y)
		self.k = kws.pop("k",[.01,.01])
		self.damping = kws.pop("damping", [.92,.92])
		Body.__init__(self,*args,**kws)
	def update_physics(self):
		# horizontal spring
		Fx = -self.k[0] * (self.coords[0]-self.size[0])
		self.accel[0] = Fx / self.mass
		self.vel[0] *= self.damping[0]
		# vertical spring
		Fy = -self.k[1] * (self.coords[1]-self.size[1])
		self.accel[1] = Fy / self.mass
		self.vel[1] *= self.damping[1]

		Body.update_physics(self)

class FalseTextFade(ui.Text):
	FADE_IN = 0
	FADE_OUT = 1
	FADE_STATE_IN = 0
	FADE_STATE_END = 1
	def __init__(self, *args, **kws):
		self.increment = int(kws.pop("increment",1))
		self.fade_mode = kws.pop("mode",FalseTextFade.FADE_IN)
		self.fade_state = FalseTextFade.FADE_STATE_IN
		self.fade_max = kws.pop("fade_max",255)
		self.fade_min = kws.pop("fade_min", 0)
		self.color = kws.pop("color",[255,255,255])
		ui.Text.__init__(self, *args, **kws)
	def update(self, **kws):
		if self.fade_state == FalseTextFade.FADE_STATE_END:
			ui.Text.update(self)
			return

		if self.fade_mode == FalseTextFade.FADE_IN:
			for i in range(3):
				if self.color[i] < self.fade_max:
					self.color[i] += self.increment
				else:
					self.fade_state = FalseTextFade.FADE_STATE_END
		elif self.fade_mode == FalseTextFade.FADE_OUT:
			for i in range(3):
				if self.color[i] > self.fade_min:
					self.color[i] -= self.increment
				else:
					self.fade_state = FalseTextFade.FADE_STATE_END

		# fixme: the value must be cleaned

		self.style["fill"] = "#%02x%02x%02x" % (self.color[0],
			self.color[1],self.color[2])
		ui.Text.update(self)

if __name__ == "__main__":
	top = base.Window("centralized","escapable","fullscreen")
	top["cursor"] = "none"
	ca = base.tk.Canvas(top,bg="black",
		highlightthickness=0)
	base.default_pack(ca)

	l = FalseTextFade(ca,top.get_screen_size()[0]/2,
		top.get_screen_size()[1]/2-20,fill="",
		text="Lightk presents",
		font=("TkDefaultFont",15,"bold"),
		mode=FalseTextFade.FADE_IN,
		color=[0,0,0],
		fade_max=150,stipple="gray12",no_shadow=True)
	l2 = FalseTextFade(ca,top.get_screen_size()[0]/2,
		top.get_screen_size()[1]/2+20,fill="",
		text="End",
		font=("TkDefaultFont",25,"bold"),
		mode=FalseTextFade.FADE_IN,
		color=[0,0,0],
		fade_max=180,stipple="gray12",no_shadow=True)
	l2.fade_state = FalseTextFade.FADE_STATE_END
	def _(*args):
		l.update()
		if l.fade_state == FalseTextFade.FADE_STATE_END:
			if l2.fade_state != FalseTextFade.FADE_STATE_IN:
				l2.fade_state = FalseTextFade.FADE_STATE_IN
			l2.update()
	top.run(_, 10)
	top.mainloop()

"""
TODOLIST:
	GAME
		Scrolling level
	UI
		WIDGETS
			Calendar
			Colorpicker
			Movablepanel
"""
