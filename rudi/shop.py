import logging
from . import device
from . import tool

class Shop():
    
    config = {}
    devices = []

    def __init__(self):
        self.deviceManager = device.DeviceManager()
        self.toolManager = tool.ToolManager()
        logging.debug("Shop started!")


    def loadConfig(self, data):    
        self.config = data

        print("\n" + "Welcome to " + self.getShopName())
        print("===================================" + "\n")

        self.deviceManager.addDevices(self.config['devices'])
        self.toolManager.addTools(self.config['tools'])
        
        logging.debug("Config loaded!")
        self.deviceManager.listAllDevices()
        self.toolManager.printToolList()


    def getShopName(self):
        return self.config['info'][0]['name']