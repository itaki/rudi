import logging
import board
import busio
from . import shop as shop
from adafruit_mcp230xx.mcp23017 import MCP23017
from adafruit_pca9685 import PCA9685
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_servokit import ServoKit

class HubManager():

    hubs = {}

    def __init__(self):
        # start up the i2c bus for all to use!
        if not shop.mock_hardware:
            self.i2c_bus = busio.I2C(board.SCL, board.SDA)
            logging.debug(f"Created I2C bus")

    def add_hub(self, hub):
        logging.debug(f"Adding {hub['name']}")
        # this adds each hub by it's id so I can access by hub_manager['id']
        self.hubs[hub['id']] = Hub(hub, self.i2c_bus)
    
    def add_hubs_from_config(self, hubs, hardware):
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
    
    def __init__(self, hub_config, i2c_bus):
        self.id = hub_config['name']
        self.config = hub_config
        self.i2c_bus = i2c_bus

        # should do some config validation before doing the below things
        if not shop.mock_hardware:
            self.setup_gpio_expander()
            self.setup_pwm_board()
            self.setup_ad_converter()


    def setup_gpio_expander(self):
        '''
        This will setup a MCP23017
        '''
        # instantiate the GPIO expander and connect to the i2c bus
        if 'gpio_expander' in self.config: # see if there is a board in this hub
            if 'i2c_address' in self.config['gpio_expander']: # see if there is a valid address
                self.config['gpio_expander']['hex_address'] = hex(self.config['gpio_expander']['i2c_address'])
                try:
                    self.gpio_expander_board = MCP23017(self.i2c_bus, address=self.config['gpio_expander']['i2c_address']) # instantiate the board
                    logging.debug(f"Created GPIO Expander at {self.config['gpio_expander']['hex_address']} which is decimal {self.config['gpio_expander']['i2c_address']}")
                except:
                    logging.error(f"COULD NOT CREATE GPIO EXPANDER AT {self.config['gpio_expander']['hex_address']} which is decimal {self.config['gpio_expander']['i2c_address']}")
        else:
            logging.debug(f"No GPIO expander found on hub named {self.id}")


    def setup_pwm_board(self):
        # instantiate the pwm board and connect to the i2c bus
        if 'pwm_board' in self.config: # see if there is a board in this hub
            if 'i2c_address' in self.config['pwm_board']: # see if there is a valid address
                self.config['pwm_board']['hex_address'] = hex(self.config['pwm_board']['i2c_address'])
                try:
                    self.pwm_board = PCA9685(self.i2c_bus, address=self.config['pwm_board']['i2c_address']) # instantiate the board
                    if 'frequency' in self.config['pwm_board']:
                        self.pwm_board.frequency = self.config['pwm_board']['frequency']
                    else:
                        self.pwm_board.frequency = 50 # 50 is the default for servos. 100-1000 is generally used for LEDs
                    logging.debug(f"Created PWM board at {self.config['pwm_board']['hex_address']} which is decimal {self.config['pwm_board']['i2c_address']}")
                except:
                    logging.error(f"COULD NOT CREATE PWM BOARD AT {self.config['pwm_board']['hex_address']} which is decimal {self.config['pwm_board']['i2c_address']}")
        else:
            logging.debug(f"No PWM board found on hub named {self.id}")
 

    def setup_ad_converter(self):
        # instantiate the AD board and connect to the i2c bus
        if 'ad_converter' in self.config: # see if there is a board in this hub
            if 'i2c_address' in self.config['ad_converter']: # see if there is a valid address
                self.config['ad_converter']['hex_address'] = hex(self.config['ad_converter']['i2c_address'])
                try:
                    self.ad_converter = ADS.ADS1115(self.i2c_bus, address=self.config['ad_converter']['i2c_address']) # instantiate the board
                    logging.debug(f"Created PWM board at {self.config['ad_converter']['hex_address']} which is decimal {self.config['ad_converter']['i2c_address']}")
                except:
                    logging.error(f"COULD NOT CREATE AD CONVERTER AT {self.config['ad_converter']['hex_address']} which is decimal {self.config['ad_converter']['i2c_address']}")
        else:
            logging.debug(f"No PWM board found on hub named {self.id}")
