import logging
from rudi.device import Device
from . import shop

## DO: Use self.config dictionary object to access device config data
## DON'T Override __init__(), use on_init() instead as needed (and if you declare on_init make sure to emit the ready event)


class SimpleButton(Device):

    def on_init(self):
        self.register_event("PRESSED")

        # add code here to setup hardware connection
        # GPIO.whatever(self.config.connection.whatever)

        # when button press is detected, do this:
        # self.emit_event("PRESSED", {})

        self.emit_event("READY", {})


class LedLight(Device):

    light_is_on = False

    auto_turn_enable = True
    auto_turn_off_duration = 300
    
    devices_who_are_on = []

    def on_init(self):
        self.register_event("TURNED_ON")
        self.register_event("TURNED_OFF")

        self.register_action("TURN_ON", "turn_on_light")
        self.register_action("TURN_OFF_SOFT", "turn_off_light_soft")
        self.register_action("TURN_OFF_HARD", "turn_off_light_hard")

        # add code to override auto turnoff defualt values if found in preferences

        # add code to start a counter for when to turn off light

        # add code to tell GPIO to turn off the light when the counter is reached 

        # add code to reset counter when new events are heards

        # add code here to setup hardware connection
        # GPIO.whatever(self.config.connection.whatever)

        self.emit_event("READY", {})
    
    def turn_on_light(self) :
        # do GPIO stuff to turn on light
        self.light_is_on = True
        self.emit_event("TURNED_ON", {})
    
    def turn_off_light_soft(self) :
        # determine if the light should really be turned off
        # if so call:
        self.turn_off_light_hard()


    def turn_off_light_hard(self) :
        # do GPIO stuff to turn off light
        self.light_is_on = False
        self.emit_event("TURNED_OFF", {})



class VoltageDetector(Device):
    
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
    


class DustCollector(Device):

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
    

class Gate(Device):

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