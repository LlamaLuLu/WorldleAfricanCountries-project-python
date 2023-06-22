# gets co-ords of where mouse clicks on screen:
import turtle as t

def get_mouse_click_coord(x, y):
    print(x, y)

t.onscreenclick(get_mouse_click_coord)
t.mainloop()
