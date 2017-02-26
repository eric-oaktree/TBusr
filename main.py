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

#red = 13 yellow = 6 green = 27
def convert(color):
    if color == 'red':
        return 13
    elif color == 'yellow':
        return 6
    elif color == 'green':
        return 27

def on(color):
    pin = convert(color)
    GPIO.output(pin,GPIO.HIGH)

def off(color):
    pin = convert(color)
    GPIO.output(pin,GPIO.LOW)

def blink(color):
    pin = convert(color)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(1)

def cont(red, yellow, green):
    t = 0
    if red == 'on' and yellow == 'off' and green == 'blink':
        on(red)
        off(yellow)
        while t < 30:
            blink(green)
            t = t + 1
    if red == 'on' and yellow == 'blink' and green == 'off':
        on(red)
        off(green)
        while t < 30:
            blink(yellow)
            t = t + 1
    if red == 'blink' and yellow == 'off' and green == 'off':
        off(yellow)
        off(green)
        while t < 30:
            blink(red)
            t = t + 1
    if red == 'off' and yellow == 'on' and green == 'blink':
        on(yellow)
        off(red)
        while t < 30:
            blink(green)
            t = t + 1
    if red == 'blink' and yellow == 'on' and green == 'off':
        on(yellow)
        off(green)
        while t < 30:
            blink(red)
            t = t + 1
    if red == 'off' and yellow == 'blink' and green == 'off':
        off(red)
        off(green)
        while t < 30:
            blink(yellow)
            t = t + 1
    if red == 'blink' and yellow == 'off' and green == 'on':
        on(green)
        off(yellow)
        while t < 30:
            blink(red)
            t = t + 1
    if red == 'off' and yellow == 'blink' and green == 'on':
        on(green)
        off(red)
        while t < 30:
            blink(yellow)
            t = t + 1
    if red == 'off' and yellow == 'off' and green == 'blink':
        off(red)
        off(yellow)
        while t < 30:
            blink(green)
            t = t + 1

def light(nBus, aBus):
    #next bus is under 5 and after bus is under 5
    if nBus <= 5 and aBus <= 5:
        cont('on', 'off', 'blink')
    #next bus is under 5 and after bus is under 10
    elif nBus <= 5 and aBus <= 10:
        cont('on', 'blink', 'off')
    #next bus is under 5 and after bus is over 10
    elif nBus <= 5 and aBus > 10:
        cont('blink', 'off', 'off')
    #next bus is under 10 and after bus is under 5
    elif nBus <= 10 and aBus <= 5:
        cont('off', 'on', 'blink')
    #next bus is under 10  and after bus is under 10
    elif nBus <= 10 and aBus <= 10:
        cont('off', 'blink', 'off')
    #next bus is under 10 and after bus is over 10
    elif nBus <= 10 and aBus > 10:
        cont('blink', 'on', 'off')
    #next bus is over 10 and after bus is under 5
    elif nBus > 10 and aBus <= 5:
        cont('off', 'off', 'blink')
    #next bus is over 10 and after bus is under 10
    elif nBus > 10 and aBus <= 10:
        cont('off', 'blink', 'on')
    #next bus is over 10 and after bus is over 10
    elif nBus > 10 and aBus > 10:
        cont('blink', 'off', 'on')
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

    elif mode() == 2:
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
