#!/usr/bin/python3
#main loop of the program, calls the crawler module and sends results to the GPIO

import crawler
from datetime import datetime

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#upper red
GPIO.setup(13,GPIO.OUT)
#upper yellow
GPIO.setup(6,GPIO.OUT)
#upper green
GPIO.setup(27,GPIO.OUT)
#lower red
#lower yellow
#lower green

#turn all on and off
GPIO.output(13,GPIO.HIGH)
GPIO.output(6,GPIO.HIGH)
GPIO.output(27,GPIO.HIGH)
time.sleep(1)
GPIO.output(13,GPIO.LOW)
GPIO.output(6,GPIO.LOW)
GPIO.output(27,GPIO.LOW)

def mode():
    #toggles mode based on time and day
    now = datetime.today()
    wday = now.strftime('%w')
    h = now.strftime('%p')
    if (wday == '1' or wday == '2' or wday == '3' or wday == '4' or wday == '5') and h == 'AM':
        mode = 1
    else:
        mode = 2
    return mode

def light(nBus, aBus):
    if nBus <= 5:
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(6,GPIO.LOW)
        GPIO.output(27,GPIO.LOW)
        time.sleep(60)
    elif nBus <= 10:
        GPIO.output(13,GPIO.LOW)
        GPIO.output(6,GPIO.HIGH)
        GPIO.output(27,GPIO.LOW)
        time.sleep(60)
    elif nBus > 10:
        GPIO.output(13,GPIO.LOW)
        GPIO.output(6,GPIO.LOW)
        GPIO.output(27,GPIO.HIGH)
        time.sleep(60)
    else:
        t = 0
        while t < 60:
            GPIO.output(13,GPIO.HIGH)
            GPIO.output(6,GPIO.LOW)
            GPIO.output(27,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(13,GPIO.LOW)
            GPIO.output(6,GPIO.HIGH)
            GPIO.output(27,GPIO.LOW)
            t = t + 1

def main():
    if mode() == 1:
        crawler.grabber('00977')
        buses = crawler.next_bus()
        bus = buses['501']
        nBus = bus['next']
        aBus = bus['after']
        nBus = int(nBus) / 60
        aBus = int(aBus) / 60
        light(nBus, aBus)

    elif mode () == 2:
        crawler.grabber('00914')
        buses = crawler.next_bus()
        bus = buses['57']
        nBus = bus['next']
        aBus = bus['after']
        nBus = int(nBus) / 60
        aBus = int(aBus) / 60
        light(nBus, aBus)

    else:
        print('Error')

while True:
    main()
