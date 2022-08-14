import sys
import logging
import pickle
from . import shop as shop


class DeviceManager():

    trigger_devices = {}
    listener_devices = {}

    def add_trigger_device(self, device):
        logging.info("Adding trigger device: " + device['id'])
        self.trigger_devices[device["id"]] = DeviceFactory(device)

    def add_listener_device(self, device):
        logging.info("Adding listener device: " + device['id'])
        self.listener_devices[device["id"]] = DeviceFactory(device)

    def add_devices_from_config(self, devices):
        for device in devices['triggers']:
            self.add_trigger_device(device)
        for device in devices['listeners']:
            self.add_listener_device(device)

    def remove_device_by_id(self, id):
        # will look through both trigger_devices and trigger_devices collections
        logging.info("Removing device: " + id)

    def remove_all_devices(self, id):
        self.trigger_devices = []
        self.listener_devices = []
        logging.info("All devices removed!")

    def print_device_list(self):
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
    
    config = {}

    def __init__(self):
        raise Exception("The Device base class cannot be directly used")


class TriggerDevice(Device):

    def __init__(self, device_config):
        self.config = device_config
        logging.info("Trigger device added: " + self.config["label"])
        shop.ee.on(shop.ShopEvents.TRIGGER_DEVICE_START_REQUEST, self.request_listener)
        self.on_init()
    
    def on_init(self):
        # a safe place for subclasses to add init code without needed to override init
        return True

    def request_listener(self, device_id):
        # listens for trigger requests that did not come from GPIO
        if (self.config["id"] == device_id):
            logging.info(self.config["id"] + " heard trigger request")
            self.on_trigger()
    
    def hardware_listener(self):
        # TODO: place gpio listener stuff here
        self.on_trigger()
    
    def on_trigger(self):
        logging.info(self.config["id"] + " was triggered")
        shop.ee.emit(shop.ShopEvents.TRIGGER_DEVICE_STARTED, self.config["id"])


class ListenerDevice(Device):

    orig_settings = {} # used to restore device settings before a started tool's settings are applied 
    # current_tool = "" # the current tool being responded to by this listener device

    def __init__(self, device_config):
        self.config = device_config
        self.orig_settings = device_config["settings"]
        logging.info("Listener device added: " + self.config["label"])
        shop.ee.on(shop.ShopEvents.TOOL_STARTED, self.tool_start_listener)
        self.on_init()

    def on_init(self):
        # a safe place for subclasses to add init code without needed to override init
        return True
    
    def tool_start_listener(self, serialized_tool_config):

        # get incoming tool config
        incoming_tool_config = pickle.loads(serialized_tool_config)

        # load any config specific to this listener device
        for listener in incoming_tool_config["device_links"]["listeners"]:
            if listener["id"] == self.config["id"]:
                # configure tool-specific settings using device originals as starting point
                self.config["settings"] = merge_dicts(listener["settings"], self.orig_settings)
        logging.info(self.config["label"] + " heard start of " + incoming_tool_config["id"] + " tool.")
        shop.ee.emit(shop.ShopEvents.LISTENER_DEVICE_STARTED, self.config["id"])
        self.on_start()
    
    def on_start(self):
        # a safe place for subclasses to add start code without needed to override init
        return True
        

# https://stackoverflow.com/questions/20656135/python-deep-merge-dictionary-data
def merge_dicts(source, destination):

    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination


# import of specific device classes must happen after parent classes are defined above
sys.path.append('../rudi')
from rudi.listeners import *
from rudi.triggers import *