#set servo with keyboard

import curses # for keyboard
import time
import numpy as np
import board
import busio
from adafruit_servokit import ServoKit
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create single-ended input on channel 0
kit = ServoKit(channels=16)


keyboard_present = True
set_range = 90 #set the servo in the middle
adjustment = 0
def key_getter(stdscr):
    """checking for keypress"""
    stdscr.nodelay(True)  # do not wait for input when calling getch
    return stdscr.getch()

def keyboard_manager(key):
    if key == 49:
        return -10
    elif key == 50:
        return -1
    elif key == 51:
        return 1
    elif key == 52:
        return 10
    else:
        return 0




while True:
    # check the keyboard for input4
    if keyboard_present == True:  # O
        adjustment = 0
        key = curses.wrapper(key_getter)
        if key != -1:  # if nothing selected
            # prints: 'key: 97' for 'a' pressed
            #print(f'\r                           key: {key} pressed')
            # '-1' on no presses
            adjustment = keyboard_manager(key)
    if adjustment != 0:
        set_range = set_range + adjustment
        if set_range > 180:
            print("TOO HIGH!!!!!!")
            set_range = 180
        if set_range < 0: 
            print("TOO LOW!!!!!")
            set_range = 0
        
        print(f"Angle = {set_range}")
        kit.servo[0].angle = set_range
