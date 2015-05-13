#!/usr/bin/env python
# Author: Willie Lawrence
"""
'ui' has the main widget's definitions
"""
import base
import themes

def show_notification(**kws):
	"""
	"""
	# fixme
	title = kws.get("title")
	msg = kws.get("msg", None)
	theme = kws.get("theme", Themes.LIGHT_BTN)
	expire_time = kws.get("expire_time",10)

class PositionManager:
	"""
	This class manages the position of a widget according with
	the initial width and height canvas size. So, if the canvas size
	change, the position also will change.
	Example:
		1| class MyNewWidget(base.BaseDraw, ui.PositionManager)
		2| ...
		3| def update(self, **kws):
		4| 		base.BaseDraw.update(self)
		5|		base.PositionManager.update()
	If you want deactivate the 'position effect' just type:
		1| any_widget.update_proportional_pos = False
	If you want change the proportion just change the initial canvas size:
		1| any_widget.initial_canvas_size = [new_width, new_height]
		2| any_widget.initial_pos = [new_x, new_y]
	Caution:
		This class assumes that the instance has an attribute called 'canvas'
		like all base.BaseDraw's instances
	"""
	def __init__(self,ca,*args,**kws):
		ca.update_idletasks()
		self.initial_canvas_size = [ca.winfo_width(), ca.winfo_height()]
		self.initial_pos = list(args)
		self.update_proportional_pos = True
	def update(self,**kws):
		if self.update_proportional_pos:
			self.coords[0] = (self.initial_pos[0]*self.canvas.winfo_width())/self.initial_canvas_size[0]
			self.coords[1] = (self.initial_pos[1]*self.canvas.winfo_height())/self.initial_canvas_size[1]

class SizeManager:
	"""
	This class manages the size of a widget according with
	the initial widget and height canvas size. So, if the canvas size
	change, the position also will change.
	Example:
		1| class MyNewWidget(base.BaseDraw, ui.SizeManager):
		2| ...
		3| def update(self):
		4|		base.BaseDraw.update(self)
		5|		ui.SizeManager.update(self)
	If you want deactivate the 'size effect' just type:
		1| any_widget.update_proportional_size = False
	If you want change the proportion just change the initial canvas size:
		1| any_widget.initial_canvas_size = [new_width, new_height]
		2| any_widget.initial_pos = [new_x, new_y]
	Caution:
		This class assumes that the instance has an attribute called 'canvas'
		like all base.BaseDraw's instances
	"""
	def __init__(self,ca,*args,**kws):
		self.initial_canvas_size = [ca.winfo_width(), ca.winfo_height()]
		self.initial_size = [kws.get("width"),kws.get("height")]
		self.update_proportional_size = True
	def update(self):
		if self.update_proportional_size:
			self.width = (self.initial_size[0] * self.canvas.winfo_width()) / self.initial_canvas_size[0]
			self.height = (self.initial_size[1]*self.canvas.winfo_height())/self.initial_canvas_size[1]

class Text(base.Label, PositionManager):
	"""
	This class is inherited of base.Label. Off what it already has
	ui.Text adds more two effects: text shadow and relative position.
	If you don't want use shadow effect you must pass in the 'instaciation'
	the key arg 'no_shadow' = True. You also can disable it calling
	ui.Text.destroy_shadow()
	The relative-position effect is from ui.PositionManager class. So,
	if you want disable it just switch the ui.Text.update_proportional_pos
	value to 'False'.
	Caution:
		ui.Text.shadow it's a base.Label instance. When you update your
		ui.Text instance you also update the shadow (if it exists). The
		shadow is in the layer below ui.Text's layer. So, caution to don't
		'dismember' the text shadow. Case you do that, you can fix calling
		ui.Text.to_raise or ui.Text.to_lower methods.
		DON'T SWITCH THE UI.TEXT.NO_SHADOW VALUE MANUALLY.
	"""
	def __init__(self, ca, *args, **kws):
		self.no_shadow = kws.pop("no_shadow", False)
		if not self.no_shadow:
			self.shadow = base.Label(ca,*args,**kws)
			self.shadow.increase = [1,1]
			self.shadow.fill = "white"
		base.Label.__init__(self, ca,*args, **kws)
		PositionManager.__init__(self,ca,*args,**kws)
		self.update()
	def update(self, **kws):
		PositionManager.update(self)
		if not self.no_shadow:
			self.shadow.coords[0] = self.coords[0]+self.shadow.increase[0]
			self.shadow.coords[1] = self.coords[1]+self.shadow.increase[1]
			self.shadow.style = dict(self.style)
			self.shadow.style["fill"] = self.shadow.fill
			self.shadow.update()
		base.Label.update(self)
	def to_raise(self):
		if not self.no_shadow:
			self.shadow.to_raise()
		base.Label.to_raise(self)
	def destroy(self):
		base.Label.destroy(self)
		if not self.no_shadow:
			self.destroy_shadow()
	def to_lower(self):
		base.Label.to_lower(self)
		if not self.no_shadow:
			self.shadow.to_lower()
	def destroy_shadow(self):
		self.shadow.destroy()
		self.no_shadow = True
		# self.update()

class SimpleButton(base.RoundedRectangle):
	def __init__(self,ca, *xy, **kws):
		_text = kws.pop("text", "")
		_no_shadow = kws.pop("no_shadow", False)
		self.theme = kws.pop("theme", themes.LIGHT_BTN)
		self.image = kws.pop("image", None)
		self.image_position = kws.pop("image_position", [0, 0])
		base.RoundedRectangle.__init__(self, ca, *xy, **kws)
		self.text = Text(ca, self.coords[0]+self.width/2,
			self.coords[1]+self.height/2,anchor="center",
			text=_text, no_shadow=_no_shadow)
		self.text.update_proportional_pos = False

		self.bind("<Motion>", self._motion, "+")
		self.bind("<B1-Motion>", self._click, "+")
		self.bind("<ButtonRelease-1>", self._motion, "+")
		self.bind("<1>", self._click, "+")
		self.bind("<Leave>", self._release, "+")

		self.text.bind("<Motion>", self._motion, "+")
		self.text.bind("<B1-Motion>", self._click, "+")
		self.text.bind("<ButtonRelease-1>", self._motion, "+")
		self.text.bind("<1>", self._click, "+")
		self.text.bind("<Leave>", self._release, "+")
		if self.image:
			self.image.bind("<Motion>", self._motion, "+")
			self.image.bind("<B1-Motion>", self._click, "+")
			self.image.bind("<ButtonRelease-1>", self._motion, "+")
			self.image.bind("<1>", self._click, "+")
			self.image.bind("<Leave>", self._release, "+")

		self._release()
	def _motion(self, *args):
		self.text.style = self.theme[0].get("over", {})
		self.style = self.theme[1].get("over", {})
		self.update()
	def _release(self, *args):
		self.text.style = self.theme[0].get("normal", {})
		self.style = self.theme[1].get("normal", {})
		self.update()
	def _click(self, *args):
		self.text.style = self.theme[0].get("clicked", {})
		self.style = self.theme[1].get("clicked", {})
		self.update()
	def bind(self, *args, **kws):
		self.text.bind(*args,**kws)
		if self.image:
			self.image.bind(*args,**kws)
		base.RoundedRectangle.bind(self, *args, **kws)
	def update(self,**kws):
		self.text.coords = [self.coords[0]+self.width/2, self.coords[1]+self.height/2]
		self.text.update()
		if self.image:
			self.image.coords = [
				self.coords[0]+self.image_position[0],
				self.coords[1]+self.image_position[1]
			]
			self.image.update()
		self.to_raise()
		self.text.to_raise()
		if self.image:
			self.image.to_raise()
		base.RoundedRectangle.update(self)

class uiFrame(base.Widget,PositionManager,SizeManager):
	def __init__(self, ca,*args, **kws):
		self.frame = base.tk.Frame(ca,width=kws.get("width"),
			height=kws.get("height"),relief="flat",border=0,
			highlightthickness=0)
		self.width = kws.get("width")
		self.height = kws.get("height")
		kws.update(window=self.frame)
		self.frame.pack_propagate(0) # tanto faz chamar ou nao
		PositionManager.__init__(self,ca,*args,**kws)
		SizeManager.__init__(self,ca,*args,**kws)
		base.Widget.__init__(self,ca,*args,**kws)
	def pack_widget(self, widget):
		widget.pack(expand="yes",fill="both")
	def update(self, **kws):
		PositionManager.update(self)
		SizeManager.update(self)
		self.style.update(width=self.width,height=self.height)
		base.Widget.update(self)

class lighTkWidget(uiFrame):
	"""
	Puts theme styling to Tkinter widgets
	"""
	def __init__(self,ca,*args,**kws):
		self.theme = kws.pop("theme", {})
		self.widget = None
		uiFrame.__init__(self,ca,*args,**kws)
	def init_bind(self):
		self.widget.bind("<Motion>", self._motion, "+")
		self.widget.bind("<B1-Motion>", self._click, "+")
		self.widget.bind("<ButtonRelease-1>", self._motion, "+")
		self.widget.bind("<1>", self._click,"+")
		self.widget.bind("<Leave>", self._release, "+")
	def _motion(self,*args):
		self.widget.configure(**self.theme.get("over",{}))
	def _release(self,*args):
		self.widget.configure(**self.theme.get("normal",{}))
	def _click(self,*args):
		self.widget.configure(**self.theme.get("clicked",{}))

class tkEntry(lighTkWidget):
	"""
	Default Tkinter.Entry lightk version
	"""
	def __init__(self,ca,*args,**kws):
		lighTkWidget.__init__(self,ca,*args,**kws)
		self.widget = base.tk.Entry(self.frame,**self.theme.get("normal",{}))
		self.pack_widget(self.widget)
		self.init_bind()
		self._release() # just to update

class tkText(lighTkWidget):
	"""
	Default Tkinter.Text lightk version
	"""
	def __init__(self,ca,*args,**kws):
		lighTkWidget.__init__(self,ca,*args,**kws)
		self.widget = base.tk.Text(self.frame,**self.theme.get("normal",{}))
		self.pack_widget(self.widget)
		self.init_bind()
		self._release()

class tkButton(lighTkWidget):
	"""
	Default Tkinter.Button lightk version
	"""
	def __init__(self,ca,*args,**kws):
		lighTkWidget.__init__(self,ca,*args,**kws)
		self.widget = base.tk.Button(self.frame,**self.theme.get("normal",{}))
		self.pack_widget(self.widget)
		self.init_bind()
		self._release()

class tkLabel(lighTkWidget):
	"""
	Default Tkinter.Label lightk version
	"""
	def __init__(self,ca,*args,**kws):
		lighTkWidget.__init__(self,ca,*args,**kws)
		self.widget = base.tk.Label(self.frame,**self.theme.get("normal",{}))
		self.pack_widget(self.widget)
		self.init_bind()
		self._release()

class ImageButton(base.Image, PositionManager):
	def __init__(self, ca, *xy, **kws):
		self.theme = kws.pop("theme")
		_text = kws.pop("text", "")
		if not kws.get("tk_photo", False):
			kws["tk_photo"] = self.theme[1]["normal"]
		base.Image.__init__(self,ca,*xy,**kws)
		PositionManager.__init__(self,ca,*xy,**kws)
		self.text = base.Label(ca, self.coords[0]+self.tk_photo.width()/2,
			self.coords[1]+self.tk_photo.height()/2,anchor="center",
			text=_text)
		self.bind("<Motion>", self._motion, "+")
		self.bind("<B1-Motion>", self._click, "+")
		self.bind("<ButtonRelease-1>", self._motion, "+")
		self.bind("<1>", self._click, "+")
		self.bind("<Leave>", self._release, "+")

		self.text.bind("<Motion>", self._motion, "+")
		self.text.bind("<B1-Motion>", self._click, "+")
		self.text.bind("<ButtonRelease-1>", self._motion, "+")
		self.text.bind("<1>", self._click, "+")
		self.text.bind("<Leave>", self._release, "+")

		# only for update
		self._release()
	def _motion(self, *args):
		self.tk_photo = self.theme[1]["over"]
		self.text.style = self.theme[0].get("over", {})
		self.text.update()
		self.update()
	def _release(self,*args):
		self.tk_photo = self.theme[1]["normal"]
		self.text.style = self.theme[0].get("normal", {})
		self.text.update()
		self.update()
	def _click(self, *args):
		self.tk_photo = self.theme[1]["clicked"]
		self.text.style = self.theme[0].get("clicked", {})
		self.text.update()
		self.update()
	def update(self,**kws):
		PositionManager.update(self)
		self.text.coords = [self.coords[0]+self.tk_photo.width()/2,
		self.coords[1]+self.tk_photo.height()/2]
		self.text.update()

		self.to_raise()
		self.text.to_raise()

		base.Image.update(self)

class Button(SimpleButton, PositionManager, SizeManager):
	"""
	The only diference to ui.SimpleButton is that
	this class has the scalable effect.
		see: update_proportional_(size|pos)
	You only must call 'ui.Button.update' method
	"""
	def __init__(self, ca, *args, **kws):
		PositionManager.__init__(self,ca,*args,**kws)
		SizeManager.__init__(self,ca,*args,**kws)
		SimpleButton.__init__(self,ca, *args, **kws)
	def update(self,**kws):
		PositionManager.update(self)
		SizeManager.update(self)
		SimpleButton.update(self)

class Scrollbar(base.RoundedRectangle):
	# fixme: proportional(pos|size)
	def __init__(self, ca,*args,**kws):
		self.__minit = [None, None] # used to save the initial mouse coords
		self.bar = Button(ca,*args,**kws)
		self.command = None # tk naming
		self.bar.update_proportional_size = False
		self.bar.update_proportional_pos = False
		base.RoundedRectangle.__init__(self,ca,*args,**kws)
		self.bar.update() # raise it
		self.bar.bind("<B1-Motion>", self._grab, "+")
		self.bar.bind("<ButtonRelease-1>", self.__clear_mouse_pos, "+")
		self.bar.bind("<1>", self.init_mouse_pos, "+")
	def init_mouse_pos(self,*args):
		self.__minit[0] = args[0].x - float(self.bar.coords[0])
		self.__minit[1] = args[0].y - float(self.bar.coords[1])
		print "[init]", self.__minit
	def __clear_mouse_pos(self,*args):
		self.__minit = [None, None]
		print "[clear]", self.__minit
	def set(self, fraction_1, fraction_2):
		# fixme: documentar melhor
		fraction_1 = float(fraction_1)
		fraction_2 = float(fraction_2)
		y_pos = self.height * fraction_1
		self.bar.coords[1] = self.coords[1] + y_pos
		second_pos = (self.height*fraction_2) + self.coords[1]
		self.bar.height = second_pos - self.bar.coords[1]
	def update(self,**kws):
		base.RoundedRectangle.update(self)
		self.bar.update() # only position
	def _grab(self,*args):
		# if not self.__minit[0]:
		# 	self.init_mouse_pos(*args)
		# 	return
		mpos = [args[0].x, args[0].y]
		bar_nw = mpos[1] - self.__minit[1]
		if self.command:
			H = self.height
			h = float(self.bar.height)
			c = bar_nw / (H-h)
			print c
			self.command("moveto", c)
		# print bar_nw

class PopWindow(base.tk.Toplevel):
	def __init__(self,*args,**kws):
		base.tk.Toplevel.__init__(self,*args,**kws)
		self._initial_config()
	def _initial_config(self):
		self.overrideredirect(True)
		self.canvas = base.tk.Canvas(self)
		self.canvas.pack(expand="yes",fill="both")
		self.canvas.bind("<Escape>", lambda e : self.withdraw(), "+")
		self.focus_force()
		self.canvas.focus_force()
	def set_size(self,width,height):
		self.geometry("%dx%d" % (width,height))
	def set_pos(self,x,y):
		self.geometry("+%d+%d" % (x,y))

class MenuGroup(base.RoundedRectangle, PositionManager, SizeManager):
	"""
	MenuGroup is a canvas widget that inherits of base.RoundedRectangle.
	You can associate a button to a MenuGroup. This button will be replaced
	in the canvas area.
	ATTRIBUTES
		padx: The horizontal padding of all buttons in relation to background
		pady: The vertical padding of all buttons in relation to background
		commands: a simple list with all buttons inside it
		theme: the default theme that will be used to create a button
			If you use MenuGroup.add_command this will be the default theme
			[obsviously you can change it]. You also can call the
			MenuGroup.commands.append method. If you choose this you can associate
			a already created button [with your own theme], but for this you need
			call MenuGroup.update method
		orient: The orientation of MenuGroup. Must be 'vertical' or 'horizontal'
		(You can use the alias base.tk.VERTICAL or base.tk.HORIZONTAL)
	"""
	def __init__(self,*args,**kws):
		self.padx = kws.pop("padx",0)
		self.pady = kws.pop("pady",0)
		self.orient = kws.pop("orient", base.tk.VERTICAL)
		self.commands = list()
		self.theme = kws.pop("theme",themes.LIGHT_BTN)
		base.RoundedRectangle.__init__(self,*args,**kws)
		PositionManager.__init__(self,*args,**kws)
		SizeManager.__init__(self,*args,**kws)
		self._initial_config()
	def _initial_config(self):
		self.style = self.theme[1]["over"]
		self.update()
	def add_command(self,**kws):
		"""
		The kws are the 'keyword args' that you will pass in ui.Button creation
		This method returns the index of button created inside MenuGroup.commands
		"""
		self.commands.append(Button(self.canvas,0,
				0,width=0,height=0,theme=self.theme,radius=self.radius,**kws)
		)
		self.commands[-1].update_proportional_pos = False
		self.commands[-1].update_proportional_size = False
		self.update_commands()
		return len(self.commands)
	def update_commands(self):
		"""
		'Commands' it's a list with all buttons. This method
		changes the width,height and the positions of all these.
		Caution: This method is called automatically when you call
		MenuGroup.update
		"""
		len_btns = len(self.commands)
		if not len_btns:
			return
		if self.orient == base.tk.VERTICAL:
			btn_height = (self.height - self.pady*2) / float(len_btns)
			for i in range(len_btns):
				btn = self.commands[i]
				btn.width = self.width - (self.padx*2)
				btn.height = btn_height
				btn.coords[0] = self.coords[0]+self.padx
				btn.coords[1] = self.coords[1]+self.pady + (i*btn_height)
				btn.radius = [0,0,0,0]
				btn.update()
			# updating radius
			self.commands[0].radius[0] = self.radius[0]
			self.commands[0].radius[-1] = self.radius[-1]
			self.commands[0].update()
			self.commands[-1].radius[1] = self.radius[1]
			self.commands[-1].radius[2] = self.radius[2]
			self.commands[-1].update()
		elif self.orient == base.tk.HORIZONTAL:
			btn_width = (self.width - self.padx*2) / float(len_btns)
			for i in range(len_btns):
				btn = self.commands[i]
				btn.width = btn_width
				btn.height = self.height - (self.pady*2)
				btn.coords[0] = self.coords[0]+self.padx + (i*btn_width)
				btn.coords[1] = self.coords[1]+self.pady
				btn.radius = [0,0,0,0]
				btn.update()
			# updating radius
			self.commands[0].radius[0] = self.radius[0]
			self.commands[0].radius[1] = self.radius[1]
			self.commands[0].update()
			self.commands[-1].radius[2] = self.radius[2]
			self.commands[-1].radius[3] = self.radius[3]
			self.commands[-1].update()
		else:
			raise ValueError("Orient attribute must be 'vertical' or 'horizontal' it is %s" % (self.orient))
	def update(self,**kws):
		PositionManager.update(self)
		SizeManager.update(self)
		base.RoundedRectangle.update(self)
		self.update_commands()

class PopMenu(PopWindow):
	"""
	Use this class if you want create a pop menu
	Example:
		1| pop_menu = PopMenu()
		2| pop_menu.add_command(text="Open file")
		3| pop_menu.get_last_command().bind("<1>", my_handler, "+")
		4| pop_menu.pop(300,400)
	Caution:
		Avoid create an instance of ui.PopMenu in the method that will put it
		in the screen. First create an instance (and it will not be showed in
		the screen) and show it calling ui.PopMenu.pop method separately. This
		procedure will make sure that the PopMenu will not be duplicated in
		window (unless you wish this). See: examples/pop_menu.py
	"""
	def __init__(self,*args,**kws):
		self.width = kws.pop("width",300)
		self.height = kws.pop("height",300)
		PopWindow.__init__(self,*args,**kws)
		self.withdraw()
		self.canvas.update_idletasks()
		self.menu_group = MenuGroup(self.canvas,0,0,width=self.width,height=self.height)
		self.menu_group.update_proportional_size = False
		self.menu_group.update_proportional_pos = False
	def update(self):
		"""
		Use this method if want change the width and/or height of popmenu.
		"""
		self.geometry("%dx%d" % (self.width+1,self.height+1)) # the increase fix the size border problem
		self.menu_group.width = self.width
		self.menu_group.height = self.height
		self.menu_group.update()
		PopWindow.update(self)
	def pop(self,x,y):
		"""
		This method shows the menu in x,y coordenates.
		"""
		self.update()
		self.canvas.focus_force()
		self.menu_group.update()
		self.geometry("+%d+%d" % (x,y))
		self.deiconify()
	def add_command(self,**kws):
		"""
		This method adds a command to ui.PopMenu.menu_group instance and
		binds to the last button created a function that withdraw the
		PopMenu.
		Caution:
			Try always use this method to add a command.
		"""
		self.menu_group.add_command(**kws)
		self.get_last().bind("<ButtonRelease-1>",lambda e : self.withdraw(), "+")
	def get_last(self):
		"""
		Returns the last button command
		"""
		return self.menu_group.commands[-1]
	def withdraw(self,*args,**kws):
		# override just for back (force the focus) to the master
		# this fix the focus linux problem
		PopWindow.withdraw(self)
		self.master.focus_force()
		
##########################################################################################
class test(Button):
	def __init__(self,*args,**kws):
		self.progress = kws.pop("progress",0.0)
		Button.__init__(self,*args,**kws)
		self.bar = Button(*args,**kws)
		self.bar.theme = list(self.bar.theme) # just to copy
		self.bar.update_proportional_pos = False
		self.bar.update_proportional_size = False
	def update(self,**kws):
		if self.progress < 0.0:
			self.progress = 0.0
		elif self.progress > 1.0:
			self.progress = 1.0
		Button.update(self,**kws)
		self.update_progress()
	def update_progress(self,*args):
		if not self.bar:
			return
		self.bar.radius = self.radius
		self.bar.height = self.height
		self.bar.width = self.width * self.progress
		self.bar.coords = self.coords
		self.bar.update()

class newProgress(Button):
	def __init__(self,ca,*args,**kws):
		self.progress = kws.pop("progress",0.0)
		self.progress_bar = Button(ca,*args,**kws)
		self.progress_bar.theme = list(self.progress_bar.theme)
		self.progress_bar.update_proportional_pos = False
		self.progress_bar.update_proportional_size = False
		Button.__init__(self,ca,*args,**kws)
		self.update()
	def update(self,**kws):
		if self.progress < 0.0:
			self.progress = 0.0
		elif self.progress > 1.0:
			self.progress = 1.0
		Button.update(self)
		self.progress_bar.radius = self.radius
		self.progress_bar.height = self.height
		self.progress_bar.width = self.width * self.progress
		self.progress_bar.coords = self.coords
		self.progress_bar.update()
	def update_progress(self,*args):
		self.progress_bar.radius = self.radius
		self.progress_bar.height = self.height
		self.progress_bar.width = self.width * self.progress
		self.progress_bar.coords = self.coords
		self.progress_bar.update()

class Progressbar(base.RoundedRectangle):
	# fixme: transformar tanto o progress como o rec como ui.Button
	def __init__(self, ca,*xy,**kws):
		self.progress_color = kws.pop("progress_color", "#f00")
		self.progress = kws.pop("progress", 0)
		base.RoundedRectangle.__init__(self, ca, *xy, **kws)
		self.progress_rec = base.RoundedRectangle(ca,
			self.coords[0],self.coords[1],self.width,self.height,fill=self.progress_color)
		self.update()
	def update(self,**kws):
		if self.progress < 0.0:
			self.progress = 0.0
		elif self.progress > 1.0:
			self.progress = 1.0
		self.update_progress()
		base.RoundedRectangle.update(self)
	def update_progress(self):
		"""
		fixme: translate better
		This method updates the drawing of progressbar marker.
		Override it to custom this widget.
		"""
		# default implementation
		# copy of same radius
		# self.progress_rec.radius = self.radius
		# self.progress_rec.style.update(fill=self.progress_color)
		# self.progress_rec.height = self.height
		# self.progress_rec.width = self.width * self.progress
		# self.progress_rec.coords = self.coords
		# self.progress_rec.update()
		RADIUS = self.height + 5
		x_pos = self.width * self.progress
		self.progress_rec.coords[0] = x_pos - RADIUS + self.coords[0]
		self.progress_rec.coords[1] = self.coords[1] - RADIUS
		self.progress_rec.width = RADIUS * 2
		self.progress_rec.height = RADIUS * 2
		self.progress_rec.radius = [6,6,6,6]
		self.progress_rec.style = themes.LIGHT_BTN[1]["over"]
		self.progress_rec.update()

if __name__ == "__main__":
	top = base.Window("centralized","escapable",resizable=True)
	ca = base.tk.Canvas(top, bg="#fff",highlightthickness=0)
	ca.pack(expand="yes",fill="both")

	t = tkEntry(ca,0,0,anchor="nw",width=200,height=35,theme=themes.DARK_ENTRY)

	h = MenuGroup(ca,300,300,width=200,height=150,radius=[10,10,10,10],padx=5,
		pady=5,orient=base.tk.VERTICAL)
	h.add_command(text="Testing")
	h.add_command(text="Other")
	pop = PopMenu()
	pop.canvas.config(highlightthickness=0)
	pop.menu_group.theme = themes.YOUTUBE_BTN
	pop.add_command(text="Back")
	pop.add_command(text="Forward")
	pop.add_command(text="Reload")
	pop.add_command(text="Save as")
	pop.add_command(text="Print")
	def __pop(*r):
		pop.pop(*top.get_mouse_pos())
	ca.bind("<3>",__pop,"+")
	h.add_command(text="Another")
	##################################################################################################
	b = SimpleButton(ca, 30,130,width=100,height=40,text="ok", theme=themes.WINDOWS_8_BLUE_BTN,radius=[5,5,5,5])
	def _cre(*args):
		# don't do that
		f = PopWindow(top)
		f.canvas.config(bg="white",highlightthickness=0)
		canvas_x = ca.winfo_rootx()
		canvas_y = ca.winfo_rooty()
		f.set_pos(canvas_x+b.coords[0],canvas_y+b.coords[1]+b.height)
		f.set_size(300,300)
		m = MenuGroup(f.canvas,0,0,width=300,height=300,theme=themes.DARK_BTN)
		m.add_command(text="New File",no_shadow=0)
		m.add_command(text="Open File",no_shadow=0)
		m.add_command(text="Open Folder",no_shadow=0)
		m.add_command(text="Open Recent",no_shadow=0)
		m.add_command(text="Reopen with Encoding",no_shadow=0)
		m.add_command(text="New view into File",no_shadow=0)
		m.add_command(text="Save",no_shadow=0)
	b.bind("<1>",_cre,"+")
	tkEntry(ca,10,20,anchor="nw",width=30,height=35,theme=themes.LIGHT_ENTRY)
	tkEntry(ca,290,20,anchor="nw",width=200,height=35,theme=themes.GOOGLE_ENTRY)

	SimpleButton(ca, 30,230,width=50,height=40,text="1", theme=themes.LIGHT_BTN,radius=[10,0,0,0])
	SimpleButton(ca, 80,235,width=50,height=40,text="2", theme=themes.LIGHT_BTN)
	SimpleButton(ca, 130,230,width=50,height=40,text="3", theme=themes.LIGHT_BTN)
	SimpleButton(ca, 180,235,width=50,height=40,text="4", theme=themes.LIGHT_BTN, radius=[0,0,10,10])

	aga = newProgress(ca,300,250,width=250,height=4,progress=0.1)
	aga.progress_bar.theme = themes.DARK_BTN
	aga.update()

	ju = test(ca,300,300,width=250,height=4,progress=0.5)
	# ju.bar.theme = list(themes.DARK_BTN)
	ju._release()

	p = Progressbar(ca, 200,200,progress=0, height=2,width=200,fill="white")
	# p.style = themes.LIGHT_BTN[1]["normal"]
	p.update()
	def _(*__):
		p.progress += .01
		p.update()
	top.bind("<1>", _, "+")
	b.update()
	top.mainloop()

# TODO: Entry themes
# colocar a opcao the shadowtextem Button
# PopMenu
# Table
# Notify
