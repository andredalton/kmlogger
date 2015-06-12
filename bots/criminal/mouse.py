__author__ = 'avale'

from os import walk, path
from evdev import InputDevice, ecodes, UInput
from pymouse import PyMouse
from select import select
from threading import Thread
from time import sleep

INPUTDIR = '/dev/input/'

class MouseListener:
    def call_me(self, position):
        raise NotImplementedError

class MouseWatcher(Thread):
    def __init__(self, listener=MouseListener()):
        Thread.__init__(self)
        self.m = PyMouse()
        self.ui = UInput()
        self.devices = []
        self.running = True
        self.lastPosition = None
        self.device_search()
        self.listener = listener

    def stop(self):
        print "Desligando mouse."
        self.running = False

    def device_search(self):
        devices_list = []
        files = []
        for (dirpath, dirnames, filenames) in walk(INPUTDIR):
            files.extend(filenames)
            break
        for f in files:
            try:
                dev = InputDevice(path.join(INPUTDIR, f))
                keymap = dev.capabilities().get(1)
                if ecodes.BTN_MOUSE in keymap and ecodes.BTN_LEFT in keymap:
                    devices_list.append(dev)
            except (IOError, OSError, TypeError):
                pass
        self.devices = {dev.fd: dev for dev in devices_list}

    def run(self):
        while self.running:
            r,w,x = select(self.devices, [], [])
            for fd in r:
                if not self.running:
                    break
                for event in self.devices[fd].read():
                    if event.type == ecodes.EV_KEY and event.value == 1:
                        self.lastPosition = self.m.position()
                        if self.listener.__class__ != MouseListener:
                            self.listener.call_me(self.lastPosition)
        self.ui.close()

if __name__ == "__main__":
    class Mouse(MouseListener):
        def call_me(self, position):
            print position

    print "Teste do MouseWatcher, 15s:"
    m = Mouse()
    ml = MouseWatcher(m)
    ml.start()
    print "Inicio"
    sleep(15)
    print "Acorda"
    ml.stop()
    print ml.lastPosition