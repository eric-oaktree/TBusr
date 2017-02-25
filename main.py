#!/usr/bin/python3
#main loop of the program, calls the crawler module and sends results to the GPIO

import crawler
from datetime import datetime

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
