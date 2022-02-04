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


    def loadConfig(self, config):    
        if not self.validate_config(config):
            return False
        self.config = config

        print("\n" + "Welcome to " + self.getShopName())
        print("===================================" + "\n")

        self.deviceManager.addDevices(self.config['devices'])
        self.toolManager.addTools(self.config['tools'])
        
        logging.debug("Config loaded!")
        self.deviceManager.printDeviceList()
        self.toolManager.printToolList()


    def getShopName(self):
        return self.config['info'][0]['name']
    
    def validate_config(self, config): #
        '''Receives loaded config file and validates it to make sure it's validates
        Currently only checks for logging level and if it's not in the config file, will return False
        
        Returns True if valid. False if invalid'''
        try:
            LOG_LEVEL = config['env'][0]['logging_level']
            return True
        except:
            #logging.debug("no logging level set in config file") # I don't think this line will work since there is no logging level
            print("No logging level set in config file")
            return False

