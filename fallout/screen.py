# coding=utf-8
__author__ = 'andre'

from Xlib import display
import Xlib
from pymouse import PyMouse
import time

def press(button=1):
    Xlib.X.ButtonPress
    Xlib.ext.xtest.fake_input(display, Xlib.X.ButtonPress, button)
    display.sync()

def release(button=1):
    Xlib.ext.xtest.fake_input(display, Xlib.X.ButtonRelease, button)
    display.sync()

def zoom_out():
    m = PyMouse()
    (x, y) = m.position()
    m.move(700, 700)
    press()
    # m.move(200, 100)
    # m.move(300, 100)
    # m.move(400, 100)
    # m.move(500, 100)
    release()
    # m.move(x, y)

def main():
    time.sleep(5)
    zoom_out()
    # try:
    #     img_width = gtk.gdk.screen_width()
    #     img_height = gtk.gdk.screen_height()
    #
    #     screengrab = gtk.gdk.Pixbuf(
    #         gtk.gdk.COLORSPACE_RGB,
    #         False,
    #         8,
    #         img_width,
    #         img_height
    #     )
    # m.move(400, 100)
    # m.move(500, 100)
    m.release(700, 700, 1)
    # m.move(x, y)

def main():
    time.sleep(5)
    zoom_out()
    # try:
    #     img_width = gtk.gdk.screen_width()
    #     img_height = gtk.gdk.screen_height()
    #
    #     screengrab = gtk.gdk.Pixbuf(
    #         gtk.gdk.COLORSPACE_RGB,
    #         False,
    #         8,
    #         img_width,
    #         img_height
    #     )
    #
    #     screengrab.get_from_drawable(
    #         gtk.gdk.get_default_root_window(),
    #         gtk.gdk.colormap_get_system(),
    #         0, 0, 0, 0,
    #         img_width,
    #         img_height
    #     )
    #
    # except:
    #     print "Failed taking screenshot"
    #     exit()
    #
    # print "Converting to PIL image ..."

    # final_screengrab = Image.frombuffer(
    #     "RGB",
    #     (img_width, img_height),
    #     screengrab.get_pixels(),
    #     "raw",
    #     "RGB",
    #     screengrab.get_rowstride(),
    #     1
    # )
    # final_screengrab.show()

    # print screengrab.pixel_array()

if __name__ == "__main__":
    main()
