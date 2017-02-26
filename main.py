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
        routes = crawler.active_routes()
    else:
        mode = 2
    return mode

def light(nBus, aBus):
    #next bus is under 5 and after bus is under 5
    if nBus <= 5 and aBus <= 5:
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(6,GPIO.LOW)
        t = 0
        while t < 60:
            GPIO.output(27,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(27,GPIO.LOW)
            time.sleep(1)
            t = t + 1
    #next bus is under 5 and after bus is under 10
    elif nBus <= 5 and aBus <= 10:
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(27,GPIO.LOW)
        t = 0
        while t < 60:
            GPIO.output(6,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(6,GPIO.LOW)
            time.sleep(1)
            t = t + 1
    #next bus is under 5 and after bus is over 10
    elif nBus <= 5 and aBus > 10:
        GPIO.output(6,GPIO.LOW)
        GPIO.output(27,GPIO.LOW)
        t = 0
        while t < 60:
            GPIO.output(13,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(13,GPIO.LOW)
            time.sleep(1)
            t = t + 1
    #next bus is under 10 and after bus is under 5
    elif nBus <= 10 and aBus <= 5:
        GPIO.output(13,GPIO.LOW)
        GPIO.output(6,GPIO.HIGH)
        t = 0
        while t < 60:
            GPIO.output(27,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(27,GPIO.LOW)
            time.sleep(1)
            t = t + 1
    #next bus is under 10  and after bus is under 10
    elif nBus <= 10 and aBus <= 10:
        GPIO.output(13,GPIO.LOW)
        GPIO.output(27,GPIO.LOW)
        t = 0
        while t < 60:
            GPIO.output(6,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(6,GPIO.LOW)
            time.sleep(1)
            t = t + 1
    #next bus is under 10 and after bus is over 10
    elif nBus <= 10 and aBus > 10:
        GPIO.output(27,GPIO.LOW)
        GPIO.output(6,GPIO.HIGH)
        t = 0
        while t < 60:
            GPIO.output(13,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(13,GPIO.LOW)
            time.sleep(1)
            t = t + 1
    #next bus is over 10 and after bus is under 5
    elif nBus > 10 and aBus <= 5:
        GPIO.output(13,GPIO.LOW)
        GPIO.output(6,GPIO.LOW)
        t = 0
        while t < 60:
            GPIO.output(27,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(27,GPIO.LOW)
            time.sleep(1)
            t = t + 1
    #next bus is over 10 and after bus is under 10
    elif nBus > 10 and aBus <= 10:
        GPIO.output(27,GPIO.HIGH)
        GPIO.output(13,GPIO.LOW)
        t = 0
        while t < 60:
            GPIO.output(6,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(6,GPIO.LOW)
            time.sleep(1)
            t = t + 1
    #next bus is over 10 and after bus is over 10
    elif nBus > 10 and aBus > 10:
        GPIO.output(27,GPIO.HIGH)
        GPIO.output(6,GPIO.LOW)
        t = 0
        while t < 60:
            GPIO.output(13,GPIO.HIGH)
            time.sleep(1)
            t = t + 1
            GPIO.output(13,GPIO.LOW)
            time.sleep(1)
            t = t + 1
    #errors
    elif nBus == 'er' and aBus == 'er':
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
    else:
        print('Error')

def main():
    if mode() == 1:
        crawler.grabber('00977')
        buses = crawler.next_bus()
        bus = buses['501']
        if bus != 'Inactive'
            nBus = bus['next']
            aBus = bus['after']
            aBus = (int(aBus) - int(nBus)) / 60
            nBus = int(nBus) / 60
            light(nBus, aBus)
        else:
            nBus = 'er'
            aBus = 'er'



    elif mode () == 2:
        crawler.grabber('00914')
        buses = crawler.next_bus()
        bus = buses['57']
        if bus != 'Inactive'
            nBus = bus['next']
            aBus = bus['after']
            aBus = (int(aBus) - int(nBus)) / 60
            nBus = int(nBus) / 60
            light(nBus, aBus)
        else:
            nBus = 'er'
            aBus = 'er'

    else:
        print('Error')

while True:
    main()
