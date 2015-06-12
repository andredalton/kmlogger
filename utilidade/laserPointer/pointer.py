#!/usr/bin/env python
__author__ = 'avale'

"""

Programa para fazer com que o controle/laser projetado para PowerPoint funcione com arquivos PDF.
Device ID 1223:3f66 SKYCABLE ENTERPRISE. CO., LTD.

"""

from os import walk, path
from evdev import InputDevice, ecodes, UInput, list_devices, categorize
from select import select
from threading import Thread

INPUTDIR = '/dev/input/'

class PointerWatcher(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ui = UInput()
        self.devices = []
        self.running = True
        self.device_search()

    def device_search(self):
        devices_list = []
        files = []
        for (dirpath, dirnames, filenames) in walk(INPUTDIR):
            files.extend(filenames)
            break
        for f in files:
            try:
                dev = InputDevice(path.join(INPUTDIR, f))
                if dev.name == "W WirelessUSB":
                    devices_list.append(dev)
            except (IOError, OSError, TypeError):
                pass
        self.devices = {dev.fd: dev for dev in devices_list}

    def run(self):
        c = 0
        if len(self.devices) > 0:
            while self.running:
                r,w,x = select(self.devices, [], [])
                for fd in r:
                    try:
                        for event in self.devices[fd].read():
                            if event.code == ecodes.KEY_UP and event.value == 1:
                                self.ui.write(ecodes.EV_KEY, ecodes.KEY_DOWN, 1)
                                self.ui.write(ecodes.EV_KEY, ecodes.KEY_DOWN, 0)
                                self.ui.write(ecodes.EV_KEY, ecodes.KEY_LEFT, 1)
                                self.ui.write(ecodes.EV_KEY, ecodes.KEY_LEFT, 0)
                                self.ui.syn()
                                c += 1
                            elif event.code == ecodes.KEY_DOWN and event.value == 1:
                                self.ui.write(ecodes.EV_KEY, ecodes.KEY_UP, 1)
                                self.ui.write(ecodes.EV_KEY, ecodes.KEY_UP, 0)
                                self.ui.write(ecodes.EV_KEY, ecodes.KEY_RIGHT, 1)
                                self.ui.write(ecodes.EV_KEY, ecodes.KEY_RIGHT, 0)
                                self.ui.syn()
                                c -= 1
                    except IOError:
                        self.running = False
                        break
        self.ui.close()

if __name__ == "__main__":
    p = PointerWatcher()
    p.start()
    p.join()