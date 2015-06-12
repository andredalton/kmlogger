__author__ = 'avale'

import numpy as np
import pyscreenshot as ImageGrab
import hashlib
import time
from mouse import MouseWatcher
from threading import Thread
import sys

class ScreenListener:
    def call_me(self, md5screen, new, position):
        raise NotImplementedError

class ScreenWatcher(Thread):
    PINI = (400, 940)                                     # Inicio da area dos botoes
    PEND = (1365, 1065)                                   # Termino da area dos botoes
    BUTTONPOS = (1200, 895, 1370, 930)                    # Posicao de algum botao estatico da tela
    BUTTOMMD5 = "a52f4fe619774a1e21502dc92806f082"        # Hash md5 do botao
    THR = 240                                             # Constante para o threshold
    CHANGETIME = 2.0                                      # Tempo para troca do botao
    STARTTIME = 4.0                                       # Tempo para iniciar a tela do jogo

    def __init__(self, listener=ScreenListener()):
        Thread.__init__(self)
        self.tela = None
        self.running = True
        self.mem = None
        self.enviados = []
        self.listener = listener
        self.time = []
        self.mouse = MouseWatcher()

    def stop(self):
        print "Desligando screen."
        self.running = False
        self.mouse.stop()

    def start(self):
        Thread.start(self)
        self.mouse.start()

    def run(self):
        while self.running:
            try:
                self.tela = ImageGrab.grab()
                width, height = self.tela.size
                token = self.tela.crop((width/2-50, height/2-50, width/2+50, height/2+50))
                md5screen = hashlib.md5(token.tostring()).hexdigest()
                button = self.tela.crop(self.BUTTONPOS)
                md5 = hashlib.md5(button.tostring()).hexdigest()
                if md5 == self.BUTTOMMD5:
                    print "Jogando"
                    h = self.PEND[1] - self.PINI[1]
                    w = self.PEND[0] - self.PINI[0]
                    md5 = []
                    for i in range(3):
                        for j in range(2):
                            a = self.tela.crop((self.PINI[0]+i*w/3, self.PINI[1]+j*h/2, self.PINI[0]+(i+1)*w/3, self.PINI[1]+(j+1)*h/2))
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
                    now = time.time()
                    if self.mem is not None:
                        for i in range(len(md5)):
                            if self.mem[i] != md5[i]:
                                if now - self.time[i] > self.CHANGETIME:
                                    if self.listener.__class__ != ScreenListener:
                                        self.listener.call_me(md5screen, self.mem[i], self.mouse.lastPosition)
                                self.time[i] = now
                                self.enviados[i] = False
                            elif not self.enviados[i] and now - self.time[i] > self.CHANGETIME:
                                if self.listener.__class__ != ScreenListener:
                                    if self.listener.call_me(md5screen, md5[i]):
                                        self.time[i] = now
                                    else:
                                        self.enviados[i] = True
                                else:
                                    self.enviados[i] = True
                    else:
                        for i in range(len(md5)):
                            self.time.append(now+self.STARTTIME-self.CHANGETIME)
                            self.enviados.append(False)
                    self.mem = md5
                else:
                    self.mem = None
                    self.enviados = []
                    self.time = []
                    print "Sem jogo"
            except (KeyboardInterrupt, IndexError):
                self.stop()


if __name__ == "__main__":
    sw = ScreenWatcher()
    print "Iniciando observcao por 20s."
    sw.start()
    time.sleep(20)
    sw.stop()