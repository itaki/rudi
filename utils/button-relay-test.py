import gpiozero
from signal import pause

relay = gpiozero.OutputDevice(21)
button = gpiozero.Button(20)

button.when_pressed = relay.on
button.when_released = relay.off

pause()