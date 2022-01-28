import logging
from . import device

class Shop():
    
    config = {}
    devices = []

    def __init__(self):
        #self.deviceManager = device.DeviceManager()
        logging.debug("Shop started!")


    def loadConfig(self, data):    
        self.config = data

        print("\n" + "Welcome to " + self.getShopName())
        print("===================================" + "\n")

        for item in self.config['devices']:
            self.devices.append(device.Device(item['id']))
        
        logging.debug("Config loaded!")
        self.listDevices()


    def listDevices(self):
        print("\n" + "Registered devices:")
        for device in self.devices:
            print("- " + device.id)


    def getShopName(self):
        return self.config['info'][0]['name']
