import logging
from rudi.device import ListenerDevice

#### Add custom listener devices below!

class DustCollector(ListenerDevice):

    minimum_runtime_minutes = 10

    def __init__(self, device):
        self.initial_config = device

        if "minimum_runtime_minutes" in device["defaults"]:
            self.minimum_runtime_minutes = self.defaults["minimum_runtime_minutes"]
            logging.debug("Setting default minimum_runtime_minutes for " + self.label + " to " + self.minimum_runtime_minutes)
        
        logging.debug("Listener Device added: " + self.initial_config["label"])

class Gate(ListenerDevice):

    open_pwm = ""
    closed_pwm = ""

    def __init__(self, device):
        self.initial_config = device

        if "open_pwm" in device["defaults"]:
            self.open_pwm = self.initial_config["defaults"]["open_pwm"]
            logging.debug("Setting open_pwm for " + self.initial_config["label"] + " to " + self.open_pwm)
        
        if "closed_pwm" in device["defaults"]:
            self.closed_pwm = self.initial_config["defaults"]["closed_pwm"]
            logging.debug("Setting closed_pwm for " + self.initial_config["label"] + " to " + self.closed_pwm)
        
        logging.debug("Listener Device added: " + self.initial_config["label"])