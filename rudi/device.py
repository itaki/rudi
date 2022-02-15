import sys
import logging

class DeviceManager():

    trigger_devices = {}
    listener_devices = {}

    def add_trigger_device(self, device):
        logging.debug("Adding trigger device: " + device['id'])
        self.trigger_devices[device["id"]] = DeviceFactory(device)

    def add_listener_device(self, device):
        logging.debug("Adding listener device: " + device['id'])
        self.listener_devices[device["id"]] = DeviceFactory(device)

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

    # would love to make this fully dynamic to not need the classmap
    # inspiration: https://python-course.eu/oop/dynamically-creating-classes-with-type.php

    classmap = {
        'TriggerDevice': TriggerDevice,
        'ListenerDevice': ListenerDevice,
        'VoltageDetector': VoltageDetector,
        'DustCollector': DustCollector,
        'Gate': Gate
    }
    return classmap[device["type"]](device)


class Device():
    
    initial_config = {}

    def __init__(self, device):
        self.initial_config = device
        logging.debug("Device added: " + self.initial_config["label"])


class TriggerDevice(Device):
    
    def on_trigger(self, source):
        logging.debug(self.initial_config["label"] + " detected a trigger event from device: " + source)


class ListenerDevice(Device):

    current_tool = "" # the most recent tool to be responded to by this device
    
    def on_tool_start(self, tool):
        self.current_tool = tool
        logging.debug(self.initial_config["label"] + " responding to start of " + self.current_tool + " tool.")


# import of specific device classes must happen after parent classes are defined above
sys.path.append('../rudi')
from rudi.listeners import *
from rudi.triggers import *