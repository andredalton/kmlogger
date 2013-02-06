from __future__ import with_statement
from evdev import InputDevice, categorize, ecodes, list_devices, UInput
from pymouse import PyMouse
from select import select

import pprint
import cPickle as pickle
import time
import contextlib
import sys

@contextlib.contextmanager
def handler():
    try:
        yield
    except Exception, e:
        return


def saveLog(data):
	pickle.dump( data, open('event.pkl', 'wb'), -1)
	
def getLog():
	return pickle.load(open('event.pkl', 'rb'))

def playHistory(h):
	i = 1
	for now in history:
		m.move( now.get("mouse")[0], now.get("mouse")[1])
		if now.get("event").type == ecodes.EV_KEY:
			ui.write(ecodes.EV_KEY, now.get("event").code, now.get("event").value)
			ui.syn()
		if i < len(history):
			time.sleep(float(history[i].get("event").sec - now.get("event").sec)+float(history[i].get("event").usec - now.get("event").usec)/1000000)
		i += 1

devicesList = []

for i in range(0, 20):
	with handler():
		dev = InputDevice('/dev/input/event'+str(i))
		keymap = dev.capabilities().get(1)
		# Verificando se e um mouse com dois botoes
		if ecodes.BTN_MOUSE in keymap and ecodes.BTN_RIGHT in keymap:
			print ( "Mouse: " + dev.name )
			devicesList.append(dev)
		# Procurando um teclado apropriado
		if ecodes.KEY_DELETE in keymap and ecodes.KEY_PLAYPAUSE in keymap and ecodes.KEY_RIGHTCTRL in keymap and ecodes.KEY_LEFTCTRL in keymap and ecodes.KEY_F12 in keymap and ecodes.KEY_S:
			print ( "Teclado: " + dev.name )
			devicesList.append(dev)

m = PyMouse()

ui = UInput()

devices = {dev.fd : dev for dev in devicesList}

copy	= False
play	= False
start	= False

history = []

while True:
	r,w,x = select(devices, [], [])
	for fd in r:
		for event in devices[fd].read():
#			print(event)
#			print(categorize(event))
			
			# F5 - salva os eventos
			if not copy and not play and event.type == ecodes.EV_KEY and event.value == 00 and event.code == ecodes.KEY_F5:
				print "\rSalvando               "
				saveLog(history)
			# F6 - carrega os eventos.
			elif not copy and not play and event.type == ecodes.EV_KEY and event.value == 00 and event.code == ecodes.KEY_F6:
				print "\rCarregando              "
				history = getLog()
			# F7 - roda uma vez.
			elif not copy and not play and event.type == ecodes.EV_KEY and event.value == 00 and event.code == ecodes.KEY_F7:
				print "\rPlay               "
				playHistory(history)
				
			# F12 - Inicia e finaliza gravacao
			elif event.type == ecodes.EV_KEY and event.code == ecodes.KEY_F12 and event.value == 00:
				if copy:
					print "\rFinalizado"
					copy = False
				else:
					start = m.position()
					if len(history)==0:
						print "\rGravando             "
					else:
						print "\rRegravando        "
						history = []
					copy = True

			# grava movimento caso esteja gravando
			elif event.type == ecodes.EV_SYN and event.code == 00 and event.value == 00 and copy:
				history.append( {"mouse": m.position(), "event": event} )
				
			# PlayStop - Play caso nao esteja gravando
			elif event.type == ecodes.EV_KEY and event.code == ecodes.KEY_PLAYPAUSE and event.value == 00 and not copy and not play:
				print "\nplay forever"
				while True:
					playHistory(history)
			# PlayStop - Para caso esteja tocando
			elif event.type == ecodes.EV_KEY and event.code == ecodes.KEY_PLAYPAUSE and event.value == 00 and not copy and play:
				print "stop"
				play = False
				
			# Grava todas as teclas de mouse e teclado
			elif copy and event.type == ecodes.EV_KEY and event.code != ecodes.KEY_F12:
				history.append( {"mouse": m.position(), "event": event} )
				
ui.close()