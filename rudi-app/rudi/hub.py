import sys
import logging
import board
import busio
import digitalio
import MCP23017
from . import shop as shop

class HubManager():

    i2c_bus = {}
    hubs = {}

    def __init__(self):
        # start up the i2c bus for all to use!
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)

    def add_hub(self, hub):
        logging.debug(f"Adding {hub['name']}")
        self.hubs[hub["id"]] = Hub(hub)
    
    def add_hubs_from_config(self, hubs):
        for hub in hubs:
            self.add_hub(hub)
    
    def get_hub_by_id(self, hub_id):
        '''
        # example usage from within a device class: 
        my_hub = HubManager.get_hub_by_id('mitre-hub')
        my_pin = my_hub.gpio_expander_board.get_pin(7)
        my_pin.pull_down_or_whatever
        '''
        return self.hubs[hub_id]
        

class Hub():
    
    config = {} # populated from config file at time of instantiation

    gpio_expander_board = {}
    
    def __init__(self, hub_config):
        self.config = hub_config

        # should do some config validation before doing the below things
        self.setup_gpio_expander()
        self.setup_pwm_board()
        self.setup_ad_converter()
    
    def setup_gpio_expander(self):

        # instantiate the gpio extender board and connect to the i2c bus
        self.gpio_expander_board = MCP23017(HubManager.i2c_bus, self.config['gpio_expander']['i2c_address'])
    
    def setup_pwm_board(self):

        # instantiate the pwm board and connect to the i2c bus
        foo = "bar"
    
    def setup_ad_converter(self):

        # instantiate the AD board and connect to the i2c bus
        foo = "bar"
