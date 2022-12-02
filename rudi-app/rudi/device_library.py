import logging
from rudi.device import Device as RudiDevice
from . import shop
from gpiozero import Device, Button, LED
from threading import Timer

## DO: Use self.config dictionary object to access device config data
## DON'T Override __init__(), use on_init() instead as needed (and if you declare on_init make sure to emit the ready event)


class SimpleButton(RudiDevice):

    def on_init(self):
        #register my valid events in case anyone asks what I can do
        self.register_event("PRESSED")

        Button.self = ''
        button = Button(self.config['connection']['address']['pin'])
        button.self = self
        button.when_pressed = self.on_press.__func__

        self.emit_event("READY", {})

    def on_press(btn): 
        btn.self.emit_event("PRESSED", {})




class Led(RudiDevice):
    '''This is a simple LED which can be on, off, toggled, forced off, blink, delayed off, and blink delayed off

        Default is simple on and off.
        Add preferences to config.json for options
        "preferences" : {
                "turn_off_delay" : 10,
                "delay_style" : "BLINK"
                "blink
            },
        delay is in seconds
        style options are "BLINK" and "SOLID" but if left blank defaults to "SOLID"'''

    turn_off_delay = 0
    delay_style = 'SOLID'
    blink_time = .5
    devices_who_want_me_on = []

    def on_init(self):
        self.register_event("TURNED_ON")
        self.register_event("TURNED_OFF")

        self.register_action("TURN_ON", self.handle_turn_on_action)
        self.register_action("TURN_OFF", self.handle_turn_off_action)
        self.register_action("TOGGLE", self.handle_toggle_action)
        self.register_action("FORCE_OFF", self.handle_force_off_action)
        self.register_action("BLINK", self.handle_blink_action)
        self.register_action("DELAYED_OFF", self.handle_delayed_off_action)
        self.register_action("DELAYED_BLINK_OFF", self.handle_delayed_blink_off_action)
        

        self.light = LED(self.config['connection']['address']['pin'])

        if 'turn_off_delay' in self.config['preferences'] :
            self.turn_off_delay = self.config['preferences']['turn_off_delay']
        else:
            self.turn_off_delay = 0

        if 'delay_style' in self.config['preferences'] :
            self.delay_style = self.config['preferences']['delay_style']
        else:
            self.delay_style = 'SOLID'

        if 'blink_time' in self.config['preferences'] :
            self.blink_time = float(self.config['preferences']['blink_time'])
        else:
            self.blink_time = .5


        # GPIO.whatever(self.config.connection.whatever)

        self.emit_event("READY", {})

    def handle_turn_on_event(self, payload) :
        self.turn_on()

    def turn_on(self) :
        #kill the timer if there is one
        self.kill_timer
        logging.debug(f"turning ON {self.config['label']}")
        self.light.on()
        self.emit_event("TURNED_ON", {})
    
    def turn_off(self, args) :
        #check to see if any other devices want me on
        if self.devices_who_want_me_on == []:
            self.force_off
        else:
            #remove device that last requested to be off from the list of devices_who_want_me_on
            logging.info(f"something asked me to be off but something else is still on so I'm not going off yet")
            
    
    def force_off(self, args) :
        #kill the timer if there is one
        self.kill_timer
        self.light.off()
        self.emit_event("TURNED_OFF", {})
            
    def toggle(self, args):
        #NEED WORK
        logging.debug(f"TOGGLING {self.config['label']}")
        if self.light.is_lit() :
            self.turn_off
        else:
            self.turn_on

    def blink(self):
        #kill the timer if there is one
        self.kill_timer
        logging.debug(f"BLINKING {self.config['label']}")
        self.light.blink(self.blink_time, self.blink_time, None, True)
        #This is probably a warning of some sort

    def delayed_off(self) :
        logging.debug(f"turning OFF {self.config['label']} after {self.turn_off_delay} seconds")
        self.timer = Timer (self.turn_off_delay, self.turn_off) 
        self.timer.start()
    
    
    def delayed_blink_off(self, args) :
        self.blink
        self.delayed_off

    
    
    def kill_timer(self, args):
        try:
            self.timer.cancel()
        except:
            pass


class SuperSimpleLedLight(RudiDevice):

    # I am a STATELESS LED light device - I always do the last thing asked of me
    # I am not very practical for real world applications

    def on_init(self):
        self.light_is_on = False
        self.register_event("TURNED_ON")
        self.register_event("TURNED_OFF")

        self.register_action("TURN_ON", self.turn_on_light)
        self.register_action("TURN_OFF", self.turn_off_light)

        self.light = LED(self.config['connection']['address']['pin'])

        self.emit_event("READY", {})
    
    def turn_on_light(self) :
        logging.debug(f"Turning ON {self.config['label']}")
        self.light.on()
        self.light_is_on = True
        self.emit_event("TURNED_ON", {})
        return True
    
    def turn_off_light(self) :
        logging.debug(f"Turning OFF {self.config['label']}")
        self.light.off()
        self.light_is_on = False
        self.emit_event("TURNED_OFF", {})
        return True

class VoltageDetector(RudiDevice):
    
    # needs more work

    baseline_voltage = 0
    sensitivity = 0

    def on_init(self):

        self.register_event("TOOL_STARTED")
        self.register_event("TOOL_STOPPED")
        self.register_event("TOOL_CHANGED")

        # add code here to setup hardware connection
        # GPIO.whatever(self.config.connection.whatever)

        # collect a series of readings and set the proper baseline and sensitivity
        # self.baseline_voltage = 1000
        # self.sensitivity = 200

        self.monitor_voltage()

        self.emit_event("READY", {})
    

    def monitor_voltage(self) :
        
        # poll GPIO for voltage readings continually
        logging.info(self.config["label"] + " is watching for voltage changes")

        # if logic decides the tool started:
        # self.emit_event("TOOL_STARTED", {})
        # self.emit_event("TOOL_CHANGED", {})

        # if logic decides the tool stopped:
        # self.emit_event("STOPPED", {})
        # self.emit_event("TOOL_CHANGED", {})
    


class DustCollector(RudiDevice):

    minimum_runtime_minutes = 10

    def on_init(self):

        self.register_event("STARTED")
        self.register_event("STOPPED")

        self.register_action("START", "start_dust_collector")
        self.register_action("STOP", "stop_dust_collector")

        if "minimum_runtime_minutes" in self.config["preferences"]:
            self.minimum_runtime_minutes = self.config["preferences"]["minimum_runtime_minutes"]

        # add code here to setup hardware connection
        # GPIO.whatever(self.config.connection.whatever)

        self.emit_event("READY", {})
    
    def start_dust_collector(self) :
        # add code here to tell GPIO to start the dust collector
        self.emit_event("STARTED", {})


    def stop_dust_collector(self) :
        # add code here to tell GPIO to stop the dust collector
        self.emit_event("STOPPED", {})
    

class Gate(RudiDevice):

    open_pwm = 0
    closed_pwm = 0

    def on_init(self):

        self.register_event("OPENED")
        self.register_event("CLOSED")
        self.register_event("CHANGED")

        self.register_action("OPEN", "open_gate")
        self.register_action("CLOSE", "close_gate")

        if "open_pwm" in self.config["preferences"]:
            self.open_pwm = self.config["preferences"]["open_pwm"]
            logging.info("Setting open_pwm for " + self.config["label"] + " to " + self.open_pwm)
        
        if "closed_pwm" in self.config["preferences"]:
            self.closed_pwm = self.config["preferences"]["closed_pwm"]
            logging.info("Setting closed_pwm for " + self.config["label"] + " to " + self.closed_pwm)
        
        # add code here to setup hardware connection
        # GPIO.whatever(self.config.connection.whatever)

        self.emit_event("READY", {})
    
    def open_gate(self):
        logging.info("Opening gate " + self.config["id"])
        
        # Add code to talk GPIO and tell it to go to the open_pwm setting
        # if successful:
        self.emit_event("OPENED", {})
        self.emit_event("CHANGED", {})
    
    def close_gate(self):
        logging.info("Closing gate " + self.config["id"])
        
        # Add code to talk GPIO and tell it to go to the closed_pwm setting
        # if successful:
        self.emit_event("CLOSED", {})
        self.emit_event("CHANGED", {})