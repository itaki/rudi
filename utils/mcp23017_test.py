import time

import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

# Create an instance of either the MCP23008 or MCP23017 class depending on
# which chip you're using:
try:
    mcp = MCP23017(i2c, address=0x20)  # MCP23008
    # mcp = MCP23017(i2c)  # MCP23017

    # Optionally change the address of the device if you set any of the A0, A1, A2
    # pins.  Specify the new address with a keyword parameter:
    # mcp = MCP23017(i2c, address=0x21)  # MCP23017 w/ A0 set

    # Now call the get_pin function to get an instance of a pin on the chip.
    # This instance will act just like a digitalio.DigitalInOut class instance
    # and has all the same properties and methods (except you can't set pull-down
    # resistors, only pull-up!).  For the MCP23008 you specify a pin number from 0
    # to 7 for the GP0...GP7 pins.  For the MCP23017 you specify a pin number from
    # 0 to 15 for the GPIOA0...GPIOA7, GPIOB0...GPIOB7 pins (i.e. pin 12 is GPIOB4).
    # pin0 = mcp.get_pin(0)
    # pin1 = mcp.get_pin(1)

    # Setup pin0 as an output that's at a high logic level.
    #mcp.get_pin(1).switch_to_output(value=True)

    # Setup pin1 as an input with a pull-up resistor enabled.  Notice you can also
    # use properties to change this state.
    #mcp.get_pin(0).direction = digitalio.Direction.INPUT
    #mcp.get_pin(0).pull = digitalio.Pull.UP

    # Setup pin 0 as input with internal pull-up resistor enabled
    # Button
    mcp.get_pin(0).direction = digitalio.Direction.INPUT
    mcp.get_pin(0).pull = digitalio.Pull.UP
    # button.direction = digitalio.Direction.INPUT
    # button.pull = digitalio.Pull.UP

    # Setup pin 1 as output
    mcp.get_pin(1).direction = digitalio.Direction.OUTPUT
    mcp.get_pin(2).direction = digitalio.Direction.OUTPUT
    mcp.get_pin(3).direction = digitalio.Direction.OUTPUT
    # led = mcp.get_pin(1)
    # led.direction = digitalio.Direction.OUTPUT

except:
    pass

# mcp = MCP23017(i2c)  # MCP23017
# Now loop blinking the pin 0 output and reading the state of pin 1 input.
while True:
    # Blink pin 0 on and then off.
    mcp.get_pin(1).value = True
    mcp.get_pin(2).value = True
    mcp.get_pin(3).value = True
    time.sleep(0.5)
    mcp.get_pin(1).value = False
    mcp.get_pin(2).value = False
    mcp.get_pin(3).value = False
    time.sleep(0.5)
    # Read pin 1 and print its state.
    print("Pin 1 is at a high level: {0}".format(mcp.get_pin(0).value))
