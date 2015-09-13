__author__ = 'avale'

import time
import pickle
from pymouse import PyMouse
from screen import ScreenListener, ScreenWatcher


class Criminal(ScreenListener):
    FILE = ".mapper"

    def __init__(self):
        try:
            self.mapper = pickle.load(open(self.FILE, 'rb'))
        except IOError:
            self.mapper = {}
        self.mapper = {}
        self.m = PyMouse()

    def __del__(self):
        print "Desligando criminal"
        pickle.dump(self.mapper, open(self.FILE, 'wb'), -1)

    def __search(self, md5screen, md5):
        print "Procurando %s em %s." % (md5, md5screen)
        try:
            self.m.click(self.mapper[md5screen][md5][0], self.mapper[md5screen][md5][1])
            print "Encontrado"
            return True
        except KeyError:
            print "Nao inserido"
            return False

    def __save(self, md5screen, md5, position):
        print "Salvando %s em %s. %s" % (md5, md5screen, position)
        try:
            self.mapper[md5screen][md5] = position
        except KeyError:
            self.mapper[md5screen] = {}
            self.mapper[md5screen][md5] = position

    def call_me(self, md5screen, md5, position=None):
        if position is None:
            return self.__search(md5screen, md5)
        self.__save(md5screen, md5, position)

if __name__ == "__main__":
    c = Criminal()
    sw = ScreenWatcher(c)
    print "Iniciando observacao"
    sw.start()
    del c
