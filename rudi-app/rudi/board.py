import sys
import logging
from . import shop as shop

class HardwareManager():

    hardware = {}

    def add_board(self, board):
        logging.debug(f"Adding {board['type']}: {board['id']} at {board['connection']}  ")
        self.hardwares[board["id"]] = BoardFactory(board)

    def add_I2C_boards_from_config(self, boards):
        for board in boards:
            self.add_board(board)

    def print_hardware_list(self):
        print("\n" + "hardwareS:" + "\n" + "===================================")
        for hardware_id in self.hardwares:
            print("    \"" + hardware_id + "\"")


def BoardFactory(hardware):

    # would love to make this fully dynamic to not need the classmap
    # inspiration: https://python-course.eu/oop/dynamically-creating-classes-with-type.php

    # or can we at least move into the hardware_library?

    classmap = {
        'pca9685': pca9685
    }
    return classmap[hardware["type"]](hardware)


class Board():
    
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
        logging.debug(f"Registering action: {self.config['id']}.{event}")
        self.events.append(event)
    
    def register_action(self, action, handler):
        # registers an action that this device class can do and provides name of handler function
        logging.debug(f"Registering action: {self.config['id']}.{action}")
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
from rudi.hardware_library import *