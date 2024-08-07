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
            if 'gpio_expander' in self.config:
                self.setup_gpio_expander()
            else:
                logging.debug(f"No GPIO expander found on hub named {self.id}")
            if 'pwm_servo' in self.config:
                self.setup_pwm_servo()
            else:
                logging.debug(f"No PWM board found on hub named {self.id}")
            if 'ad_converter' in self.config:
                self.setup_ad_converter()
            else:
                logging.debug(f"No AD converter found on hub named {self.id}")


    def setup_gpio_expander(self):
        '''
        This will setup a MCP23017
        '''
        # instantiate the GPIO expander and connect to the i2c bus
        # grab the library from hardware file
        if 'i2c_address' in self.config['gpio_expander']: # see if there is a valid address
            self.config['gpio_expander']['i2c_address'] = int(self.config['gpio_expander']['i2c_address'], 16) # this converts json HEX string to int
            try:
                self.gpio_expander_board = MCP23017(self.i2c_bus, address=self.config['gpio_expander']['i2c_address']) # instantiate the board
                logging.debug(f"Address {hex(self.config['gpio_expander']['i2c_address'])} : Created GPIO Expander : Decimal {self.config['gpio_expander']['i2c_address']}")
            except:
                logging.error(f"Address {hex(self.config['gpio_expander']['i2c_address'])} : COULD NOT CREATE GPIO EXPANDER : Decimal {self.config['gpio_expander']['i2c_address']}")

            


    def setup_pwm_servo(self):
        # instantiate the pwm board and connect to the i2c bus

        if 'i2c_address' in self.config['pwm_servo']: # see if there is a valid address
            self.config['pwm_servo']['i2c_address'] = int(self.config['pwm_servo']['i2c_address'], 16) # this converts json HEX string to int
            try:
                self.pwm_servo = PCA9685(self.i2c_bus, address=self.config['pwm_servo']['i2c_address']) # instantiate the board
                if 'frequency' in self.config['pwm_servo']:
                    self.pwm_servo.frequency = self.config['pwm_servo']['frequency']
                else:
                    self.pwm_servo.frequency = 50 # 50 is the default for servos. 100-1000 is generally used for LEDs
                logging.debug(f"Address {hex(self.config['pwm_servo']['i2c_address'])} : Created PWM board : Decimal {self.config['pwm_servo']['i2c_address']}")
            except:
                logging.error(f"Address {hex(self.config['pwm_servo']['i2c_address'])} : COULD NOT CREATE PWM BOARD : Decimal {self.config['pwm_servo']['i2c_address']}")

 

    def setup_ad_converter(self):
        # instantiate the AD board and connect to the i2c bus
        if 'i2c_address' in self.config['ad_converter']: # see if there is a valid address
            self.config['ad_converter']['i2c_address'] = int(self.config['ad_converter']['i2c_address'], 16) # this converts json HEX string to int
            try:
                self.ad_converter = ADS.ADS1115(self.i2c_bus, address=self.config['ad_converter']['i2c_address']) # instantiate the board
                logging.debug(f"Address {hex(self.config['ad_converter']['i2c_address'])} : Created AD Converter : Decimal {self.config['ad_converter']['i2c_address']}")
            except:
                logging.error(f"Address {hex(self.config['ad_converter']['i2c_address'])} : COULD NOT CREATE AD CONVERTER : Decimal {self.config['ad_converter']['i2c_address']}")
