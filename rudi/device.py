import logging

class DeviceManager():

    trigger_devices = {}
    listener_devices = {}

    def add_trigger_device(self, device):
        self.trigger_devices[device["id"]] = DeviceFactory(device)
        logging.debug("Trigger device added: " + device['id'])

    def add_listener_device(self, device):
        self.listener_devices[device["id"]] = DeviceFactory(device)
        logging.debug("Listener device added: " + device['id'])

    def add_devices_from_config(self, devices):
        for device in devices['triggers']:
            self.add_trigger_device(device)
        for device in devices['listeners']:
            self.add_listener_device(device)

    def removeDeviceById(self, id):
        # will look through both trigger_devices and trigger_devices collections
        logging.debug("Removing device: " + id)

    def removeAllDevices(self, id):
        self.trigger_devices = []
        self.listener_devices = []
        logging.debug("All devices removed!")

    def printDeviceList(self):
        print("\n" + "DEVICES:" + "\n" + "===================================")
        print("Triggers:")
        for device_id in self.trigger_devices:
            print("    \"" + device_id + "\"")
        print("\n" + "Listeners:")
        for device_id in self.listener_devices:
            print("    \"" + device_id + "\"")

def DeviceFactory(device):
    return TriggerDevice(device)



class Device():
    
    id = ""
    label = ""
    type = ""
    connection = ""

    def __init__(self, device):
        self.id = device["id"]
        self.label = device["label"]
        self.type = device["type"]
        self.connection = device["connection"]
        logging.debug("Device created: " + self.label)


class TriggerDevice(Device):
    
    def on_trigger(self):
        logging.debug("Trigger device detected: " + self.label)

class ListenerDevice(Device):

    current_tool = "" # the most recent tool to be responded to by this device
    
    def on_tool_start(self, tool):
        self.current_tool = tool
        logging.debug(self.label + " responding to start of " + self.current_tool + " tool.")

class VoltageDetector(TriggerDevice):

    base_voltage = 10

class DustCollector(ListenerDevice):

    min_runtime_sec= 180