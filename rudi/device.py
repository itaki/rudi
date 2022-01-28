import logging

"""
class DeviceManager():

    devices = []

    def addDevice(self, item):
        self.devices.append(Device(item.id))
        logging.debug("Device added: " + item.id)

    def addDevices(self, items):
        for item in items:
            self.addDevice(item)

    def removeDeviceById(self, id):
        logging.debug("Removing device: " + id)

    def removeAllDevices(self, id):
        logging.debug("Removing all devices!")

    
"""

class Device():
    
    id = ""

    def __init__(self, id):
        self.id = id
        logging.debug("Device created: " + self.id)
        