import time
from adafruit_servokit import ServoKit

# this file uses just the one import. creates a servokit object and controls it directly

# change the address to your board address
kit = ServoKit(channels=16, address=0x42)

while True:
    kit.servo[0].angle = 10 
    time.sleep(.5)      # need to sleep to give the servo time to move
    kit.servo[0].angle = 120
    time.sleep(.5)




