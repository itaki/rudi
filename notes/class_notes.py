
OUTPUT
Relay: #switches, dust_collector, lights, LEDs, 
	on
	off

PWM: #LEDs, Servos, RGBLEDs


INPUT/SENSORS
Short: #button, cutoff 

Feed: #data, voltage detector, PH Sensor, 


Timed_Relay (Relay):
	on
	off
	timed_off

Light (Timed_Relay):
	on
	off
	timed_off
	toggle

Dimmable_Light_AKA_Work_Light(Light):
	on
	off
	timed_off
	toggle
	dim

Button_Light(light) #PWM or software PWM
    on
    off
    blink
    pulse
    dim     

Gate (Servo):
	open
	close
	rattle


THINGS I ACTUALLY WANT IN MY SHOP

Light