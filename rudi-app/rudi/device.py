import sys
import logging
from . import shop as shop


class DeviceManager():

    devices = {}

    def add_device(self, device):
        logging.debug(f"Adding {device['type']}: {device['id']} at {device['connection']} " )
        self.devices[device["id"]] = DeviceFactory(device)

    def add_devices_from_config(self, devices):
        for device in devices:
            self.add_device(device)

    def print_device_list(self):
        print("\n" + "DEVICES:" + "\n" + "===================================")
        for device_id in self.devices:
            print("    \"" + device_id + "\"")


def DeviceFactory(device):

    # would love to make this fully dynamic to not need the classmap
    # inspiration: https://python-course.eu/oop/dynamically-creating-classes-with-type.php

    # or can we at least move into the device_library?

    classmap = {
        'SimpleButton': SimpleButton,
        'Led': Led,
        'SuperSimpleLedLight': SuperSimpleLedLight
    }
    return classmap[device["type"]](device)


class Device():
    
    config = {} # populated from config file at time of instantiation
    actions = {} # actions that this device CAN do, registered individually by subclass implementation
    events = [] # events that this device CAN emit, registered individually by subclass implementation

    def __init__(self, device_config):
        self.config = device_config

        self.on_init()

        #loop thru the provided config and subscribe to specified events
        for sub in self.config['subscriptions']:
            shop.em.subscribe(sub['listen_to'], sub['listen_for'], self.actions[sub['do_this']])
    
    def on_init(self):
        # a safe place for subclasses to add init code without needed to override init
        self.emit_event("READY", {})
        return True

    def register_event(self, event):
        # registers an event that this device class can emit
        logging.debug("Registering event: " + self.config['id'] + "." + event)
        self.events.append(event)
    
    def register_action(self, action, handler):
        # registers an action that this device class can do and provides name of handler function
        logging.debug("Registering action: " + self.config['id'] + "." + action)
        self.actions[action] = handler
    
    def emit_event(self, event, payload) :
        # used by subclass implementation can be used by actions or other class logic
        shop.em.emit(self.config['id'], event, payload)

    def get_actions(self):
        return self.actions
    
    def get_events(self):
        return self.events
    


# import of specific device classes must happen after parent "Device" class is defined above
sys.path.append('../rudi')
from rudi.device_library import *