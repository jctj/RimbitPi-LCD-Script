#!/usr/bin/python

from multiprocessing import Process
from lcd import infolcd
from backup import runbackup
import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings (False)
GPIO.setup (4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup (17, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def runlcd():
	infolcd()

def startbackup():
	runbackup()

def main():
	info = Process(target=runlcd)
	info.start()

	print "Press Button 4 to Run Backup"
	GPIO.wait_for_edge(4, GPIO.FALLING)
	info.terminate()
	time.sleep(0.5)

	backup = Process(target=startbackup)
	backup.start()
	backup.join()

	main()


if (__name__ == "__main__"):
	main()
