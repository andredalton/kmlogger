from __future__ import with_statement
import os
import numpy as np
from matplotlib import pyplot as plt
import pyscreenshot as ImageGrab
import cv2
import hashlib
from evdev import InputDevice, ecodes, UInput
from pymouse import PyMouse
from select import select
from threading import Thread

from subprocess import call

import cPickle as pickle
import time
import sys

FILE = ".criminal"
TIME = 1

# dev = InputDevice('/dev/input/event7')
# keymap = dev.capabilities().get(1)
# print dev.capabilities(verbose=True)
# print keymap
# sys.exit()

np.set_printoptions(threshold='nan')

class MakeClick(Thread):
    def __init__(self, lst, md5):
        Thread.__init__(self)
        self.lst = lst
        self.mapper = mapper

    def run(self):
        print "Rodando!!!!"
        print self.lst
        global mapper
        global m
        global clicking
        global atuais
        clicking = True
        for i in self.lst:
            try:
                m.click(self.mapper[md5][i][0], self.mapper[md5][i][1], 1)
                time.sleep(0.3)
            except (KeyError, TypeError):
                mapper[md5][i] = None
        atuais = set(self.lst)
        clicking = False

def searchButton(tela, botao):
    telacinza = np.array(tela.convert('L'))
    w, h = botao.shape[::-1]
    res = cv2.matchTemplate(telacinza, botao, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    return np.where(res >= threshold)

def fragmenta(tela):
    h = 1060 - 940
    w = 1365 - 400
    md5 = []
    for i in range(0, w, w/3):
        if i + w/3 > 1100:
            break
        for j in range(0, h, h/2):
            a = tela.crop((400+i, 940+j, 400+i+w/3, 940+j+h/2))
            a = np.array(a.convert('L'))
            aux = np.indices(a.shape)
            thr = a < 240
            aux[0][thr] = 0
            aux[1][thr] = 0
            lmax = np.max(aux[0])
            cmax = np.max(aux[1])
            aux[0][thr] = 1000000
            aux[1][thr] = 1000000
            lmin = np.min(aux[0])
            cmin = np.min(aux[1])

            md5.append(hashlib.md5(np.array_str(a[lmin:lmax, cmin:cmax])).hexdigest())
    return md5

def saveLog(filename, data):
    pickle.dump(data, open(filename, 'wb'), -1)

def getLog(filename):
    return pickle.load(open(filename, 'rb'))

# Inicia a busca por dispositivos de mouse
devicesList = []
for i in range(0, 20):
    try:
        dev = InputDevice('/dev/input/event'+str(i))
        keymap = dev.capabilities().get(1)
        if ecodes.BTN_MOUSE in keymap and ecodes.BTN_LEFT in keymap:
            print ("Mouse: " + dev.name )
            devicesList.append(dev)
    except (TypeError, OSError) :
        pass
devices = {dev.fd : dev for dev in devicesList}

# Handlers para eventos de mouse e eventos genericos
m = PyMouse()
ui = UInput()
botao = cv2.imread('botao.png',0)
method = cv2.TM_SQDIFF_NORMED

# Ciclo principal do programa.
start = False
clicking = False
try:
    mapper = getLog(FILE)
except IOError:
    mapper = {}
print mapper
atuais = set()
cont = 0
try:
    while True:
        r,w,x = select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                if not clicking:
                    if event.type == ecodes.EV_KEY and event.value == 1:
                        print atuais
                        if not start:
                            time.sleep(4.5)
                            tela = ImageGrab.grab()
                            loc = searchButton(tela, botao)
                            if len(loc[0]) > 0:
                                tela.save("crops/img"+str(cont)+".jpeg", "JPEG")
                                cont += 1
                                print "Inicio"
                                start = True
                                width, height = tela.size
                                crop = tela.crop((width/2-50, height/2-50, width/2+50, height/2+50))
                                md5 = hashlib.md5(crop.tostring()).hexdigest()
                                if mapper.get(md5) is None:
                                    mapper[md5] = {}
                                thr = MakeClick(fragmenta(tela), md5)
                                thr.start()
                        else:
                            time.sleep(3)
                            tela = ImageGrab.grab()
                            loc = searchButton(tela, botao)
                            if len(loc[0]) == 0:
                                print "Fim"
                                atuais = set()
                                start = False
                            else:
                                tela.save("crops/img"+str(cont)+".jpeg", "JPEG")
                                cont += 1
                                frame = fragmenta(tela)
                                antigos = atuais - set(frame)
                                for antigo in antigos:
                                    mapper[md5][antigo] = m.position()
                                thr = MakeClick(fragmenta(tela), md5)
                                thr.start()
                                print mapper[md5]
                                print "Analise"
except KeyboardInterrupt:
    saveLog(FILE, mapper)
ui.close()
