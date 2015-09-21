import Tkinter as tk

class BaseDraw:
	def __init__(self, **kws):
		self.info = kws
		self.pos = kws.pop('pos')
		self.canvas = kws.pop('canvas')
		self.width = kws.pop('width', None)
		self.height = kws.pop('height', None)
		self.name = kws.pop('name')
		self.__tags = self.generate_tags(self.name)
		self.styles = kws.pop('styles', {})
		self.styles["normal"] = self.info
	
	def switch_style(self, style_name):
		'''
		Switches the style of draw
		'''
		self.info = self.styles[style_name]
		self.update()
	
	def get_tags(self):
		'''
		Returns the 'private' tag list
		'''
		return self.__tags
	
	def generate_tags(self, name):
		'''
		Returns a list with tags of the object
		'''
		raise NotImplementedError()
	
	def update(self):
		'''
		Redraws the object
		'''
		raise NotImplementedError()
	
	def bind(self, *args, **kws):
		'''
		Binds an event to draw
		'''
		for i in self.get_tags():
			self.canvas.tag_bind(i, *args, **kws)
	
	def delete(self):
		'''
		Deletes the draw
		'''
		for i in self.get_tags():
			self.canvas.delete(i)

class Rectangle(BaseDraw):
	'''
	NW centered rectangle
	options:
		fill
		outline
		stipple
		linewidth
	'''
	def __init__(self, **kws):
		BaseDraw.__init__(self, **kws)
	
	def generate_tags(self, name):
		index = self.canvas.create_rectangle(
			self.pos[0], self.pos[1],
			self.pos[0]+self.width, self.pos[1]+self.height,
			tag=name,
			fill=self.info.get('fill') or "#000000",
			outline=self.info.get('outline') or "#000000",
			stipple=self.info.get('stipple') or '',
			width=self.info.get('linewidth') or 1
		)
		return [index] if name is None else [name]
	
	def update(self):
		self.canvas.coords(
			self.get_tags()[0],
			self.pos[0], self.pos[1],
			self.pos[0]+self.width, self.pos[1]+self.height
		)
		self.canvas.itemconfig(
			self.get_tags()[0],
			fill=self.info.get('fill') or "#000000",
			outline=self.info.get('outline') or "#000000",
			stipple=self.info.get('stipple') or '',
			width=self.info.get('linewidth') or 1
		)

class Circle(Rectangle):
	'''
	NW centered Oval
	options:
		fill
		outline
		stipple
		linewidth
	'''
	def __init__(self, **kws):
		Rectangle.__init__(self, **kws)
	
	def set_radius(self, radius):
		'''
		Sets the radius of oval
		'''
		self.width = radius
		self.height = radius
	
	def generate_tags(self, name):
		index = self.canvas.create_oval(
			self.pos[0], self.pos[1],
			self.pos[0]+self.width, self.pos[1]+self.height,
			tag=name,
			fill=self.info.get('fill') or "#000000",
			outline=self.info.get('outline') or "#000000",
			stipple=self.info.get('stipple') or '',
			width=self.info.get('linewidth') or 1
		)
		return [index] if name is None else [name]

class Line(BaseDraw):
	'''
	NW centered line
	options:
		fill
		stipple
		linewidth
		width and height ignored
	'''
	def __init__(self, **kws):
		self.end_point = kws.get('end_point')
		BaseDraw.__init__(self, **kws)
	
	def generate_tags(self, name):
		index = self.canvas.create_line(
			self.pos[0], self.pos[1],
			self.end_point[0], self.end_point[1],
			tag=name,
			fill=self.info.get('fill') or "#000000",
			stipple=self.info.get('stipple') or '',
			width=self.info.get('linewidth') or 1
		)
		return [index] if name is None else [name]
	
	def update(self):
		self.canvas.coords(
			self.get_tags()[0],
			self.pos[0], self.pos[1],
			self.end_point[0], self.end_point[1]
		)
		self.canvas.itemconfig(
			self.get_tags()[0],
			fill=self.info.get('fill') or "#000000",
			stipple=self.info.get('stipple') or '',
			width=self.info.get('linewidth') or 1
		)

class Text(BaseDraw):
	'''
	NW centered text
	options:
		fixme
	'''
	def __init__(self, **kws):
		self.text = kws.pop('text')
		BaseDraw.__init__(self, **kws)
	
	def generate_tags(self, name):
		index = self.canvas.create_text(
			self.pos[0], self.pos[1],
			tag=name,
			fill=self.info.get('fill') or "#000000",
			stipple=self.info.get('stipple') or '',
			text=self.text, font=self.info.get('font'),
			anchor=self.info.get('anchor')
		)
		return [index] if name is None else [name]
	
	def update(self):
		self.canvas.coords(
			self.get_tags()[0],
			self.pos[0], self.pos[1]
		)
		self.canvas.itemconfig(
			self.get_tags()[0],
			fill=self.info.get('fill') or "#000000",
			font=self.info.get('font'),
			anchor=self.info.get('anchor')
		)

class OldWidget(BaseDraw):
	def __init__(self, **kws):
		self.widget = kws.pop('widget')
		BaseDraw.__init__(self, **kws)
	
	def generate_tags(self, name):
		index = self.canvas.create_window(
			self.pos[0], self.pos[1],
			tag=name,
			window=self.widget,
			anchor=self.info.get('anchor')
		)
		return [index] if name is None else [name]
	
	def bind(self, *args, **kws):
		self.widget.bind(*args, **kws)
	
	def update(self):
		self.canvas.coords(
			self.get_tags()[0],
			self.pos[0], self.pos[1]
		)
		self.canvas.itemconfig(
			self.get_tags()[0],
			anchor=self.info.get('anchor'),
			window=self.widget
		)

def lerp(a,b,x):
	return a + ((b-a)*x)

def get_x(a,b,lerp_result):
	return (lerp_result-a) / (float(b)-a)

def get_rgb(r,g,b):
	return "#%02x%02x%02x" % (r,g,b)

class Gradient(BaseDraw):
	def __init__(self, **kws):
		BaseDraw.__init__(self, **kws)
	
	def generate_tags(self, name):
		indexes = []
		Dcolor = [i/256 for i in self.canvas.winfo_rgb(self.info.get('downcolor'))]
		Ucolor = [i/256 for i in self.canvas.winfo_rgb(self.info.get('upcolor'))]
		for ny in range(self.pos[1],self.height+self.pos[1]):
			xlerp = get_x(self.pos[1], self.pos[1] + self.height, ny)
			ncolor = [int(lerp(Ucolor[i], Dcolor[i], xlerp)) for i in range(3)]
			indexes.append(self.canvas.create_line(self.pos[0],ny,self.pos[0]+self.width,ny, fill=get_rgb(*ncolor),tag=name))
		if self.info.get('outline'):
			indexes.append(self.canvas.create_rectangle(self.pos[0],self.pos[1],self.pos[0]+self.width, self.pos[1]+self.height, outline=self.info.get('outline'), tag=[name,name+'outline']))
		if name:
			return [name, "outline"+name]
		else:
			return indexes

	def update(self):
		self.delete()
		self.generate_tags(self.name)

if __name__ == "__main__":
	top = tk.Tk()
	top.bind('<Escape>', lambda e:top.quit(), "+")
	canvas = tk.Canvas(top, bg="white", bd=0, highlightthickness=0, width=640,height=480)
	canvas.grid()
	rec = Gradient(pos=[100,0],width=10,height=100,canvas=canvas,name="obj1",upcolor="#eee",downcolor="#ddd",styles={"light":{"upcolor":"#00aacc", "downcolor":"#00bbdd"}})
	rec.pos[0] += 100
	rec.update()
	rec.pos[0] += 100
	rec.update()
	rec.bind('<Motion>', lambda e : rec.switch_style('light'), "+")
	rec.bind('<Leave>', lambda e : rec.switch_style('normal'), "+")
	top.mainloop()
