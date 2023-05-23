#servo hat LED tests
import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize PCA9685 module.
pca = PCA9685(i2c, address=0x42)

# Set the PWM frequency to 1000hz.
pca.frequency = 1000

# Assuming that the LED's red, green, and blue cathodes 
# are connected to PWM outputs 13, 14, and 15 respectively.
red = pca.channels[13]
green = pca.channels[14]
blue = pca.channels[15]

# to turn an LED on one would need to decrease the voltage so that the anode can go to ground
def fade_in(channel):
    """Slowly turn on an LED"""
    for i in range(100, -1, -1):
        channel.duty_cycle = int(i / 100 * 0xffff)
        time.sleep(0.01)
    

# to turn an LED off one would need to increase the voltage so that the anode is no longer grounded
def fade_out(channel):
    """Slowly turn off an LED"""
    for i in range(100):
        channel.duty_cycle = int(i / 100 * 0xffff)
        time.sleep(0.01)

# Slowly turn on red, then off
fade_in(red)
fade_out(red)

# Slowly turn on green, then off
fade_in(green)
fade_out(green)

# Slowly turn on blue, then off
fade_in(blue)
fade_out(blue)

# Slowly turn on all colors (produces white), then off
fade_in(red)
fade_in(green)
fade_in(blue)
fade_out(red)
fade_out(green)
fade_out(blue)

fade_in(red)
fade_out(red)