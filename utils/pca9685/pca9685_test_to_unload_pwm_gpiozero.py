import time
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

# Initialize I2C bus
i2c = busio.I2C(SCL, SDA)

# Set the correct I2C address for your PCA9685
pca_address = 0x42

# Initialize PCA9685 with the correct address
pca = PCA9685(i2c, address=pca_address)
pca.frequency = 50

# Custom class to interface with the PCA9685 using gpiozero's Servo class
class PCA9685Servo:
    def __init__(self, pca, channel):
        self.pca = pca
        self.channel = channel

    def set_angle(self, angle):
        pulse_width = int(4096 * ((angle * 11) + 500) / 20000)
        self.pca.channels[self.channel].duty_cycle = pulse_width

    def detach(self):
        self.pca.channels[self.channel].duty_cycle = 0

# Initialize the custom servo class for the specific channel
servo = PCA9685Servo(pca, channel=0)

# Function to set the servo angle
def set_servo_angle(servo, angle):
    servo.set_angle(angle)

# Run the servo back and forth three times
for _ in range(3):
    set_servo_angle(servo, 10)
    time.sleep(0.5)
    set_servo_angle(servo, 120)
    time.sleep(0.5)

print('I got out of there')

# Turn off the PWM signal
servo.detach()

# Cleanup
pca.deinit()

