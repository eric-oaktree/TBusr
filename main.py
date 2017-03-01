#!/usr/bin/python3
#main loop of the program, calls the crawler module and sends results to the GPIO

import crawler
from datetime import datetime
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import time

# Raspberry Pi LCD pin configuration:
lcd_rs        = 27
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4

upred = 6
upyellow = 13
upgreen = 26
downred = 16
downyellow = 12
downgreen = 5
lightpins = [upred, upyellow, upgreen, downred, downyellow, downgreen]

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#upper red
GPIO.setup(upred,GPIO.OUT)
#upper yellow
GPIO.setup(upyellow,GPIO.OUT)
#upper green
GPIO.setup(upgreen,GPIO.OUT)
#lower red
GPIO.setup(downred,GPIO.OUT)
#lower yellow
GPIO.setup(downyellow,GPIO.OUT)
#lower green
GPIO.setup(downgreen,GPIO.OUT)

#turn all on and off
def lopen():
    for pin in lightpins:
        GPIO.output(int(pin),GPIO.HIGH)
    for pin in lightpins:
        GPIO.output(int(pin),GPIO.LOW)

def reset():
    for pin in lightpins:
        GPIO.output(int(pin),GPIO.LOW)

# Print a two line message
lcd.message('TBusrrrr\nACTIVATTTEEE!')

def mode():
    #toggles mode based on time and day
    now = datetime.today()
    wday = now.strftime('%w')
    h = now.strftime('%p')
    print(wday)
    print(h)
    if (wday == '1' or wday == '2' or wday == '3' or wday == '4' or wday == '5') and h == 'AM':
        mode = 1
    else:
        mode = 2
    return mode

#red = 13 yellow = 6 green = 27
def convert(color, side):
    if color == 'red' and side == 'up':
        return upred
    elif color == 'yellow' and side == 'up':
        return upyellow
    elif color == 'green' and side == 'up':
        return upgreen
    elif color == 'red' and side == 'down':
        return downred
    elif color == 'yellow' and side == 'down':
        return downyellow
    elif color == 'green' and side == 'down':
        return downgreen

def on(color):
    pin = convert(color)
    GPIO.output(int(pin),GPIO.HIGH)

def off(color):
    pin = convert(color)
    GPIO.output(int(pin),GPIO.LOW)

def blink(color1, color2):
    pin1 = convert(color1)
    pin2 = convert(color2)
    GPIO.output(int(pin1),GPIO.HIGH)
    GPIO.output(int(pin2),GPIO.HIGH)
    time.sleep(1)
    GPIO.output(int(pin1),GPIO.LOW)
    GPIO.output(int(pin2),GPIO.LOW)
    time.sleep(1)

def assign(time, b):
    if b == 'n':
        if time == 'er'
            return 'er'
        if time <= 5:
            return 'red'
        if time <= 10:
            return 'yellow'
        if time > 10:
            return 'green'
    if b == 'a':
        if time == 'er'
            return 'er'
        if time <= 5:
            return 'green'
        if time <=10:
            return 'yellow'
        if time > 10:
            return 'red'

def light(upnBus, upaBus, dnnBus, dnaBus):
    upsol = assign(upnBus, 'n')
    dnsol = assign(dnnBus, 'n')
    upblink = assign(upaBus, 'a')
    dnblink = assign(dnaBus, 'a')
    t = 0
    while t < 30:
        if upsol == upblink and dnsol == dnblink:
            blink(upblink, dnblink)
        if upsol == upblink:
            on(dnsol)
            blink(upblink, dnblink)
        if dnsol == dnblink:
            on(upsol)
            blink(upblink, dnblink)
        else:
            on(upsol)
            on(dnsol)
            blink(upblink, dnblink)
        t = t + 1

def setbus(upstop, upline, downstop, downline):
    crawler.grabber(upstop)
    buses = crawler.next_bus()
    bus = buses[upline]
    if bus != 'Inactive':
        nBus = bus['next']
        aBus = bus['after']
        upaBus = (int(aBus) - int(nBus)) / 60
        upnBus = int(nBus) / 60
    else:
        upnBus = 'er'
        upaBus = 'er'
    crawler.grabber(downstop)
    buses = crawler.next_bus()
    bus = buses[downline]
    if bus != 'Inactive':
        nBus = bus['next']
        aBus = bus['after']
        dnaBus = (int(aBus) - int(nBus)) / 60
        dnnBus = int(nBus) / 60
    else:
        dnnBus = 'er'
        dnaBus = 'er'
    data = [upnBus, upaBus, dnnBus, dnaBus]
    return data

def main():
    reset()
    if mode() == 1:
        points = setbus('00977', '501', '00977', '503')
        lcd.message('In501: ' + str(points[0]) + 'A: ' + str(points[1]) + '\nIn503: ' + str(points[2]) + 'A: ' + str(points[3]))
        light(points[0], points[1], points[2], points[3])


    elif mode() == 2:
        points = setbus('00914', '57', '00977', '57')
        lcd.message('In57: ' + str(points[0]) + 'A: ' + str(points[1]) + '\nOut57: ' + str(points[2]) + 'A: ' + str(points[3]))
        light(points[0], points[1], points[2], points[3])

    else:
        print('Error')

while True:
    lopen()
    main()
