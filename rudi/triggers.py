import logging
from rudi.device import TriggerDevice
from . import shop

#### Add custom trigger devices below!
## DO: Use self.config dictionary object to access device config data
## DON'T Override __init__(), use on_init() instead as needed

class VoltageDetector(TriggerDevice):

    base_voltage = 10

    def on_init(self):
        logging.debug("Voltage Detector added")


class LEDButton(TriggerDevice):

    off_color = "blue"
    on_color = "red"

    def on_init(self):
        logging.debug("LED button added")

    def on_trigger(self):
        logging.debug("Turning LED button " + self.on_color)
