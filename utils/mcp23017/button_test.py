import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
import time

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP23017
mcp = MCP23017(i2c, address=0x20)

# Set up pin 0 as an input with a pull-up resistor
pin0 = mcp.get_pin(0)
pin0.direction = digitalio.Direction.INPUT
pin0.pull = digitalio.Pull.UP

# Variable to keep track of the button state
button_pressed = False

# Simple loop to detect button press and toggle state
print("Press the button connected to pin 0...")

while True:
    if not pin0.value and not button_pressed:  # Button is pressed
        print("button pressed")
        button_pressed = True  # Update the state
    elif pin0.value and button_pressed:  # Button is released
        button_pressed = False  # Reset the state

    # Add a small delay to debounce the button
    time.sleep(0.05)
