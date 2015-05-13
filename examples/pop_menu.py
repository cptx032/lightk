import sys
sys.path.extend([".","..","../.."])

from lightk import base, ui,themes
window = base.Window("escapable","fullscreen")
ca = base.tk.Canvas(window,bg="#464646",highlightthickness=0)
base.default_pack(ca)

label = ui.Text(ca,20,20,anchor="nw",text="Click with right mouse button",fill="darkgray",no_shadow=1)

pop = ui.PopMenu()
pop.canvas.config(highlightthickness=0)
pop.menu_group.theme = themes.YOUTUBE_BTN
pop.add_command(text="New File")
pop.add_command(text="Open File")
pop.add_command(text="Open Folder")
pop.add_command(text="Open Recent")
pop.add_command(text="Reopen with Encoding")
pop.add_command(text="New view into File")

def _show_menu(*args):
	pop.pop(*window.get_mouse_pos())
ca.bind("<ButtonRelease-3>", _show_menu, "+")
# ca.bind("<ButtonRelease-3>", lambda e : pop.pop(*window.get_mouse_pos()), "+") # all using only one line

window.mainloop()