# this is an effort to unload the PWM signal from the PCA9685 board so as to not burn out the servo motor
import board
import busio
import time
from adafruit_servokit import ServoKit

# Initialize the ServoKit instance with the appropriate I2C address
kit = ServoKit(channels=16, address=0x42)

# Function to turn off the PWM signal for a specific servo channel
def turn_off_pwm(servo_channel):
    kit._pca.channels[servo_channel].duty_cycle = 0

# Set the initial angle
kit.servo[0].angle = 90

# Run the servo back and forth three times and then stop
for _ in range(3):
    kit.servo[0].angle = 10 
    time.sleep(0.5)
    kit.servo[0].angle = 120
    time.sleep(0.5)

print('I got out of there')

# Turn off the PWM signal for the servo on channel 0
turn_off_pwm(0)

