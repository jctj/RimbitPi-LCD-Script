#!/usr/bin/python

from multiprocessing import Process
from lcd import infolcd
from backup import runbackup
import RPi.GPIO as GPIO
import time
from shutdown import shutdown

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings (False)
GPIO.setup (4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup (3, GPIO.IN)

def runlcd():
	infolcd()

def startbackup():
	runbackup()

def startshutdown():
	shutdown()

def main():

	info = Process(target=runlcd)

	info.start()

	while (info.is_alive() == True):
		if(GPIO.input(4) == 0):
			info.terminate()
			time.sleep(0.5)
			startbackup()
			main()

		if(GPIO.input(3) == 0):
			info.terminate()
			time.sleep(0.5)
			startshutdown()

	main()

if (__name__ == "__main__"):
	main()
