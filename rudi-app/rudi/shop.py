import logging
import os
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from . import hub
from . import device
from . import event


em = event.EventManager()
mock_hardware = os.environ.get('MOCK_HARDWARE', False)

class Shop():

    config = {}
    
    def __init__(self, shop_config, hardware):
        if not self.validate_config(shop_config):
            raise Exception("Invalid Shop Config")
        
        # Define the hub manager but don't actually build the hubs
        self.hub_manager = hub.HubManager()
        # Define the device manager but don't actually build the devices
        self.device_manager = device.DeviceManager()
        self.load_config(shop_config, hardware)
        logging.info("Shop started!")

        print(f"\nWelcome to {self.get_shop_name()}")
        print("===================================\n")

    def load_config(self, shop_config, hardware):    
        self.config = shop_config
        logging.debug("Shop Config started loading")
        self.set_hardware_mode()
        # Build the hubs
        self.hub_manager.add_hubs_from_config(self.config['hubs'], hardware)
        # Build the devices
        ####self.device_manager.add_devices_from_config(self.config['devices'])
        logging.debug("Shop Config finished loading")
    
    def validate_config(self, shop_config):
        return True
    
    def set_hardware_mode(self):
        if mock_hardware:
            logging.warning("MOCKING HARDWARE!")
            Device.pin_factory = MockFactory()
        return True

    def get_shop_name(self):
        return self.config['info'][0]['name']

