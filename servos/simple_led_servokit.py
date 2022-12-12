import time
from adafruit_servokit import ServoKit

# this tests leds using the servokit rather than pca9685

# change the address to your board address
kit = ServoKit(channels=16, address=0x42)

while True:
    kit.servo[15].angle = 10 
    time.sleep(.5)      # need to sleep to give the servo time to move
    kit.servo[15].angle = 120
    time.sleep(.5)




