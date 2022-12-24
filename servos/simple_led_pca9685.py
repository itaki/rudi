import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c, address=0x42)

hat.frequency = 60

led_channel = hat.channels[15]

# from 0x0000 to 0xffff 0 to 65535

for i in range(0xffff):
    led_channel.duty_cycle = i
    i = i+1