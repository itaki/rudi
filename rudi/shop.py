import logging
from . import device

class Shop():
    
    config = {}
    devices = []

    def __init__(self):
        self.deviceManager = device.DeviceManager()
        logging.debug("Shop started!")


    def loadConfig(self, data):    
        self.config = data

        print("\n" + "Welcome to " + self.getShopName())
        print("===================================" + "\n")

        self.deviceManager.addDevices(self.config['devices'])
        
        logging.debug("Config loaded!")
        self.deviceManager.listAllDevices()


    def getShopName(self):
        return self.config['info'][0]['name']
