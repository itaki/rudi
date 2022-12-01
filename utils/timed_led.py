from gpiozero import LED, Button
from signal import pause
from threading import Timer


button = Button(20)
on_button = Button(24)
timer_button = Button(23)

class MasterLed():
    light_is_on = False
    led = LED(21)

    def turn_off(self) :
        self.led.off()

    def turn_off_delayed(self) :
        print("going to turn off in 3 secs")
        self.timer = Timer (3, self.turn_off)
        self.timer.start()

    def turn_on(self) :
        try:
            self.timer.cancel()
        except:
            pass
        self.led.on()

my_led = MasterLed()
button.when_pressed = my_led.turn_off
on_button.when_pressed = my_led.turn_on
timer_button.when_pressed = my_led.turn_off_delayed

pause()