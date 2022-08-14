import logging
from rudi.device import ListenerDevice
from . import shop

#### Add custom listener devices below!
## DO: Use self.config dictionary object to access device config data
## DON'T Override __init__(), use on_init() instead as needed

class DustCollector(ListenerDevice):

    minimum_runtime_minutes = 10

    def on_init(self):

        if "minimum_runtime_minutes" in self.config["settings"]:
            self.minimum_runtime_minutes = self.config["settings"]["minimum_runtime_minutes"]
            logging.info("Setting default minimum_runtime_minutes for " + self.config["label"] + " to " + self.minimum_runtime_minutes)
    
    def on_start(self):
        logging.info("Starting dust collector (" + self.config["id"] + ")")
        # TODO: Talk GPIO and actually turn on dust collector


class Gate(ListenerDevice):

    open_pwm = ""
    closed_pwm = ""

    def on_init(self):

        if "open_pwm" in self.config["settings"]:
            self.open_pwm = self.config["settings"]["open_pwm"]
            logging.info("Setting open_pwm for " + self.config["label"] + " to " + self.open_pwm)
        
        if "closed_pwm" in self.config["settings"]:
            self.closed_pwm = self.config["settings"]["closed_pwm"]
            logging.info("Setting closed_pwm for " + self.config["label"] + " to " + self.closed_pwm)
    
    def on_start(self):
        logging.info("Starting gate (" + self.config["id"] + ")")
        # TODO: Talk GPIO and actually set the pwm