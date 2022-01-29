import logging

class DeviceManager():

    trigger_devices = []
    listener_devices = []

    def addTriggerDevice(self, item):
        self.trigger_devices.append(TriggerDevice(item['id']))
        logging.debug("Trigger device added: " + item['id'])

    def addListenerDevice(self, item):
        self.listener_devices.append(ListenerDevice(item['id']))
        logging.debug("Listener device added: " + item['id'])

    def addDevices(self, items):
        for item in items['triggers']:
            self.addTriggerDevice(item)
        for item in items['listeners']:
            self.addListenerDevice(item)

    def removeDeviceById(self, id):
        # will look through both trigger_devices and trigger_devices collections
        logging.debug("Removing device: " + id)

    def removeAllDevices(self, id):
        self.trigger_devices = []
        self.listener_devices = []
        logging.debug("All devices removed!")

    def listAllDevices(self):
        print("\n" + "Trigger devices:")
        for device in self.trigger_devices:
            print("- " + device.id)
        print("\n" + "Listener devices:")
        for device in self.listener_devices:
            print("- " + device.id)


class TriggerDevice():
    
    id = ""

    def __init__(self, id):
        self.id = id
        logging.debug("Trigger device created: " + self.id)

class ListenerDevice():
    
    id = ""

    def __init__(self, id):
        self.id = id
        logging.debug("Listener device created: " + self.id)
        