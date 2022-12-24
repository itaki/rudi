import logging
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from . import device
from . import event



em = event.EventManager()

class Shop():

    config = {}

    def __init__(self, shop_config):
        if not self.validate_config(shop_config):
            raise Exception("Invalid Shop Config")
        
        self.device_manager = device.DeviceManager()
        self.load_config(shop_config)
        logging.info("Shop started!")

        print(f"\nWelcome to {self.get_shop_name()}")
        print("===================================\n")

    def load_config(self, data):    
        self.config = data
        logging.debug("Shop Config started loading")
        self.set_pin_mode()
        self.device_manager.add_devices_from_config(self.config['devices'])
        logging.debug("Shop Config finished loading")
    
    def validate_config(self, shop_config):
        return True
    
    def set_pin_mode(self):
        if self.config['hardware']['GPIO']['preferences']['use_mock_pins']:
            logging.warning("USING MOCK PINS!")
            Device.pin_factory = MockFactory()
        return True

    def get_shop_name(self):
        return self.config['info'][0]['name']

