Application to run on a RPi to display when the next bus is coming.

Determines whether to look for the 501 bus or the 57 bus based on the time - changes the stop it looks at as well.

Red means the bus is under 5 minutes, yellow means under 10, green means over 10.

Blinking indicates how far the bus after the next bus is behind the next bus.  The scale is inverted, green means the bus is less than 5 minutes behind the next bus, yellow is less than 10, and red is over 10.

For example, blinking red means the bus is less than 5 minutes away and the bus after is over 10 minutes away.  Solid green and blinking yellow indicates over 10 minutes away and the bus after is less than 10 minutes behind the next bus.

Uses GPIO ports 6, 13, and 27 by default.
