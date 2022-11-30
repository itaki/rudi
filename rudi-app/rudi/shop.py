import logging
import atexit
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

        print("\n" + "Welcome to " + self.get_shop_name())
        print("===================================" + "\n")

    def load_config(self, data):    
        self.config = data
        logging.debug("Shop Config started loading")
        self.set_pin_mode()
        self.set_shutdown_mode()
        self.device_manager.add_devices_from_config(self.config['devices'])
        logging.debug("Shop Config finished loading")
    
    def validate_config(self, shop_config):
        return True
    
    def set_pin_mode(self):
        if "use_mock_pins" in self.config['hardware']:
            if self.config['hardware']['use_mock_pins']:
                Device.pin_factory = MockFactory()
    
    def set_shutdown_mode(self):
        if "reset_devices_on_exit" in self.config['hardware']:
            if self.config['hardware']['reset_devices_on_exit']:
                atexit.register(self.shutdown)

    def get_shop_name(self):
        return self.config['info'][0]['name']
    
    def shutdown(self):
        logging.debug("Shop is shutting down...")
        em.emit("shop", "SHUTDOWN", {})

