#!/usr/bin/env python
# Author: Willie Lawrence
"""
base has the basics classes for lightk.
"""
import math
import Tkinter as tk

def list_get(_list, value):
	"""
	Returns True if value is in _list. If is, so the value is
	removed from list.
	"""
	_v_in_list = value in _list
	if _v_in_list:
		_list.remove(value)
	return _v_in_list

def enable_escape(master):
	"""
	This function binds the destroying method of a window
	to Escape key. 
	"""
	master.bind("<Escape>", lambda e:master.destroy(), "+")
def default_pack(canvas):
	"""
	This function packs any widget expanding it in all sides
	"""
	canvas.pack(expand="yes", fill="both")

class Window(tk.Tk):
	def __init__(self,*args,**kargs):
		args = list(args)
		_center = list_get(args,"centralized")
		_escapable = list_get(args, "escapable")
		_fullscreen = list_get(args, "fullscreen")

		self._config = {
			"title" : kargs.pop("title", "lightk"),
			"resizable" : bool(kargs.pop("resizable", False)),
			"fullscreen" : bool(kargs.pop("fullscreen", False)),
			"overrideredirect" : bool(kargs.pop("overrideredirect", False)),
			"width" : int(kargs.pop("width", 640)),
			"height" : int(kargs.pop("height", 480)),
			"posx" : int(kargs.pop("posx", 0)),
			"posy" : int(kargs.pop("posy", 0)),
			"border" : int(kargs.pop("border", 0)),
		}
		self.kmap = {}
		tk.Tk.__init__(self, *args, **kargs)
		self.bind("<Any-Key>", self.update_kmap_press, "+")
		self.bind("<Any-KeyRelease>", self.update_kmap_release, "+")
		self.update()
		if _center:self.centralize()
		if _escapable:enable_escape(self)
		if _fullscreen:self.fullscreen()
	def update_kmap_press(self, evt):
		"""
		This method updates the state machine of keys.
		Caution: don't use it
		"""
		self.kmap[evt.keysym] = True
	def update_kmap_release(self, evt):
		"""
		This method updates the state machine of keys.
		Caution: don't use it
		"""
		self.kmap[evt.keysym] = False
	def update(self):
		"""
		This method updates the Window.
		"""
		self.title(self._config["title"])
		self.geometry("%(width)dx%(height)d+%(posx)d+%(posy)d" % self._config)
		self.config(bd=self._config["border"])
		self.resizable(self._config["resizable"],self._config["resizable"])
		self.attributes("-fullscreen", self._config["fullscreen"])
		self.overrideredirect(self._config["overrideredirect"])

		tk.Tk.update(self)
	def centralize(self):
		"""
		This method centralize the window in the screen. Its ignored
		if the window is in fullscreen mode.
		"""
		_wi = self.winfo_width()
		_he = self.winfo_height()
		_swi = self.winfo_screenwidth()
		_she = self.winfo_screenheight()
		self._config["posx"] = (_swi / 2) - (_wi / 2)
		self._config["posy"] = (_she / 2) - (_he / 2)
		self.update()
	def fullscreen(self):
		"""
		Makes the window fullscreen.
		"""
		self._config.update(width=self.winfo_screenwidth(),
			height=self.winfo_screenheight(), fullscreen=True)
		self.update()
	def run(self, event, frame_rate):
		"""
		Call 'event' function/method many times at each 'frame_rate' milisseconds.
		It works like a mainloop.
		"""
		event()
		self.after(frame_rate, lambda:self.run(event, frame_rate))
	def get_screen_size(self):
		""" Returns a list with width and height of default screen. """
		return [self.winfo_screenwidth(), self.winfo_screenheight()]
	def get_mouse_pos(self):
		""" Returns a list with the global position of mouse [in the default screen] """
		return list(self.winfo_pointerxy())
	def get_relative_mouse_pos(self):
		""" Returns a list with the mouse position relative at window nw corner. """
		p = self.winfo_pointerxy()
		r_mouse_pos = [
			p[0]-self.winfo_rootx(),
			p[1]-self.winfo_rooty()
		]
		return r_mouse_pos
	def get_width(self):
		""" Returns the current window's width"""
		return self.winfo_width()
	def get_height(self):
		""" Returns the current window's height """
		return self.winfo_height()

class BaseDraw(object):
	"""
	This class represents a basic draw in lightk.
	I think that you will never use this class, but understand how it
	works is good for understand lightk.
	"""
	def __init__(self, canvas, *coords, **style):
		_no_init = style.pop("no_init", False)
		self.canvas = canvas
		self.coords = list(coords)
		self.style = style
		self.index = None
		if not _no_init:
			self.init()
	def init(self):
		"""
		Init creates new index for object.
		If you pass the arg 'no_init' the object will not be drawed,
		so you should call obj.init() method to create a index for it.
		If the objectal ready has an index, then the object will be deleted
		and it will receive a new index.
		"""
		if self.index == None:
			self.index = self.draw()
		else:
			self.canvas.delete(self.index)
			self.index = self.draw()
		# self.update()
	def draw(self):
		""" Must return the the canvas draw's index """
		pass
	def update(self, **kws):
		"""
		This method updates the position and the attributes of an object.
		If you pass the 'idle' arg with True, so lightk will force the draw
		calling 'Tkinter.Canvas.update_idletasks' method.
		Recomendation: If you are updating a list of many objects use idle=True
		only in the last object, because this will force the updating of all:
			obj01.update()
			obj02.update()
			obj03.update(idle=True)
		"""
		if self.index:
			self.canvas.coords(self.index, *self.coords)
			self.canvas.itemconfig(self.index, **self.style)
			# @Warning
			if kws.get("idle",False):
				self.canvas.update_idletasks()
	def to_raise(self):
		"""
		This method puts the object in the top of all objects.
		Use this function if you want have certain that your
		object will be looked.
		"""
		self.canvas.tag_raise(self.index)
	def to_lower(self):
		"""
		This method puts the object in the down of all objects.
		"""
		self.canvas.lower(self.index)
	def bind(self, *args, **kargs):
		"""
		This method works like 'Tkinter.Widget.bind': binds a functions
		to an event.
		"""
		self.canvas.tag_bind(self.index, *args, **kargs)
	def destroy(self):
		"""
		This method will delete the object and clean the index to None.
		To re-activate the object call 'obj.init()'
		"""
		self.canvas.delete(self.index)
		self.index = None

class Widget(BaseDraw):
	"""
	This class represents the basics of any widget of Tkinter that will
	be drawed in a canvas.
	The 'coords' attribute has the position of widget. It will be placed
	in the canvas based in the anchor key arg [ base.Widget.style["anchor"] ]
	Needed values:
		1. Canvas instance
		2. x and y positions
	Example:
	To put an Tkinter.Button in a Canvas just type:
		1| tkinter_btn = Button(text="OK")
		2| lightk_btn_controller = base.Widget(my_canvas,10,10,window=tkinter_btn)
	"""
	def __init__(self, canvas, *xy, **kws):
		BaseDraw.__init__(self, canvas, *xy, **kws)
	def draw(self):
		return self.canvas.create_window(*self.coords, **self.style)

class Polygon(BaseDraw):
	"""
	This class represents a Polygon.
	Needed values:
		1. Canvas instance
		2. values of each point
	Example:
		1| my_polygon = base.Polygon(my_canvas, 0,0,1,1,2,3,3,fill="black" [...] )
	"""
	def __init__(self, canvas, *coords, **style):
		BaseDraw.__init__(self, canvas, *coords, **style)
	def draw(self):
		return self.canvas.create_polygon(*self.coords, **self.style)

class Line(BaseDraw):
	"""
	This class represents a single line.
	Needed values:
		1. Canvas instance
		2. 1st x,y position and 2st x,y position
	Example:
		1| my_line = base.Line(my_canvas, 0,0,100,100, fill="black" [...] )
	"""
	def __init__(self,canvas,*xy,**kws):
		BaseDraw.__init__(self,canvas,*xy,**kws)
	def draw(self):
		return self.canvas.create_line(*self.coords,**self.style)

class Rectangle(Polygon):
	"""
	This class represents a simple rectangle.
	Needed values:
		1. Canvas instance
		2. The 'nw' x,y position
	Example:
		1| my_rec = base.Rectangle(my_canvas, 0,0,width=10 [...] )
	Caution:
		The 'update' method formats the 'Rectangle.coords' field.
		This method use the two first values like x,y 'nw' position and formats
		the last two values to make the width and height. So DON'T edit it manually.
		If you want change the size of the rectangle type:
			1| my_rec.width = new_value
			2| my_rec.update()
	"""
	def __init__(self, canvas, *coords, **style):
		# The coords are the nw position
		self.width = style.pop("width", 10)
		self.height = style.pop("height", 10)
		Polygon.__init__(self, canvas, *coords, **style)
	def draw(self):
		return self.canvas.create_rectangle(self.coords[0],
			self.coords[1], self.coords[0]+self.width,
			self.coords[1]+self.height, **self.style)
	def update(self, **kws):
		self.coords = [self.coords[0],
					self.coords[1], self.coords[0]+self.width,
					self.coords[1]+self.height]
		Polygon.update(self)

def get_circle_point(cx,cy,radius,angle):
	"""
	Returns the position of a vertex2D of a circle
	which center is in [cx,cy] position and radius 'radius'
	in the angle 'angle'
	"""
	# angle in degree
	angle = math.radians(angle)
	y = math.sin(angle) * radius
	x = math.cos(angle) * radius
	x += cx
	y = cy - y
	return [x,y]

class RoundedRectangle(Polygon):
	"""
	This class represents a rounded corner rectangle.
	Needed values:
		1. Canvas instance
		2. x,y position value
	Example:
		1| my_rec = base.RoundedRectangle(my_canvas, 0,0,0,0,width=100,height=100,radius=[10,10,10,10])
	Caution:
		DON'T edit base.RoundedRectangle.coords manually.
	"""
	def __init__(self, canvas, *coords,**style):
		# nw, sw, se, ne
		self.radius = style.pop("radius",[0,0,0,0])
		self.width = int(style.pop("width",10))
		self.height = int(style.pop("height",10))
		self.level = int(style.pop("level",1))
		Polygon.__init__(self, canvas,*coords,**style)
	def get_coords(self):
		pts = []
		# NW
		if self.radius[0]:
			cx = self.coords[0] + self.radius[0]
			cy = self.coords[1] + self.radius[0]
			for i in range(90,180,self.level):
				pts.extend(get_circle_point(cx,cy,
					self.radius[0], i))
		else:
			pts.extend([self.coords[0],self.coords[1]])
		# SW
		if self.radius[1]:
			cx = self.coords[0] + self.radius[1]
			cy = self.coords[1] + self.height - self.radius[1]
			for i in range(180,270,self.level):
				pts.extend(get_circle_point(cx, cy,
					self.radius[1], i))
		else:
			pts.extend([self.coords[0],self.coords[1]+self.height])

		# SE
		if self.radius[2]:
			cx = self.coords[0]+self.width-self.radius[2]
			cy = self.coords[1]+self.height-self.radius[2]
			for i in range(270,360,self.level):
				pts.extend(get_circle_point(cx,cy,
					self.radius[2],i))
		else:
			pts.extend([self.coords[0]+self.width,
				self.coords[1]+self.height])
		# NE
		if self.radius[3]:
			cx = self.coords[0]+self.width-self.radius[3]
			cy = self.coords[1]+self.radius[3]
			for i in range(0,90,self.level):
				pts.extend(get_circle_point(cx,cy,
					self.radius[3],i))
		else:
			pts.extend([self.coords[0]+self.width,
				self.coords[1]])
		return pts
	def update(self, **kws):
		_old = self.coords
		self.coords = self.get_coords()
		Polygon.update(self)
		self.coords = _old
	def draw(self):
		return self.canvas.create_polygon(*self.get_coords(),**self.style)

class Oval(Polygon):
	"""
	This class represents an simple oval.
	Needed values:
		1. Canvas instance
		2. x,y position
	Example:
		1| my_oval = base.Oval(my_canvas, 0,0,width=100,height=100)
	"""
	def __init__(self, canvas, *coords, **style):
		# The coords are the nw position
		self.width = style.pop("width", 10)
		self.height = style.pop("height", 10)
		Polygon.__init__(self, canvas, *coords, **style)
	def draw(self):
		return self.canvas.create_oval(self.coords[0],
			self.coords[1], self.coords[0]+self.width,
			self.coords[1]+self.height, **self.style)
	def update(self, **kws):
		self.coords = [self.coords[0],
					self.coords[1], self.coords[0]+self.width,
					self.coords[1]+self.height]
		Polygon.update(self)
	def set_radius(self, radius):
		"""
		This method sets the radius of the circle
		Caution:
			This method dones't calls update method, so you must do it your self
		"""
		self.width = radius
		self.height = radius

def get_image(src):
	"""
	Checks for ImageTk module and returns the appropriate
	instance of Image.
	"""
	try:
		import ImageTk
		_img = ImageTk.PhotoImage(file=src)
		_img.zoom = _img._PhotoImage__photo.zoom
		_img.subsample = _img._PhotoImage__photo.subsample
		return _img
	except:
		return tk.PhotoImage(file=src)

class Image(BaseDraw):
	"""
	This class represents an image
	Needed values:
		1. Canvas instance
		2. x,y position
		3. 'tk_photo' or 'src' attributes
			'src' : must have a path to file
			'tk_photo' : must have an instance of PhotoImage or ImageTk.PhotoImage
			If you pass both, tk_photo has priority
	Example:
		1| my_photo = base.get_image("lenna.png")
		2| my_img = base.Image(my_canvas,0,0,anchor="nw",tk_photo=my_photo)
	To change the image you can replace base.Image.tk_photo attribute:
		1| my_img.style.tk_photo = my_new_photo
		2| my_img.update()
	Caution:
		DON'T change base.Image.style["image"] manually
	"""
	def __init__(self, canvas, *coords, **style):
		self.tk_photo = style.pop("tk_photo", None)
		if not self.tk_photo:
			self.tk_photo = get_image(style.pop("src"))
		BaseDraw.__init__(self, canvas, *coords, **style)
	def draw(self):
		return self.canvas.create_image(*self.coords, image=self.tk_photo, **self.style)
	def update(self, **kws):
		self.style["image"] = self.tk_photo
		BaseDraw.update(self)

class Label(BaseDraw):
	"""
	This class represents a simple text
	Example:
		1| my_label = base.Label(my_canvas,0,0,anchor="nw",text="My text")
	You maybe want  use 'ui.Text' class instead that class.
	"""
	def __init__(self, canvas, *coords, **style):
		BaseDraw.__init__(self, canvas, *coords, **style)
	def draw(self):
		return self.canvas.create_text(*self.coords, **self.style)