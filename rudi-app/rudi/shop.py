# from errno import EEXIST
import logging
from enum import Enum
import webbrowser
from pymitter import EventEmitter
from . import device
from . import tool
from . import event


em = event.EventManager()

class Shop():

    config = {}

    def __init__(self, shop_config):
        if not self.validate_config(shop_config):
            raise Exception("Invalid Shop Config")
        
        self.device_manager = device.DeviceManager()
        self.tool_manager = tool.ToolManager()
        self.load_config(shop_config)
        logging.info("Shop started!")

        print("\n" + "Welcome to " + self.get_shop_name())
        print("===================================" + "\n")
        #self.deviceManager.printDeviceList()
        #self.toolManager.printToolList()

    def load_config(self, data):    
        self.config = data
        self.device_manager.add_devices_from_config(self.config['devices'])
        logging.debug("Shop config finished loading")
    
    def validate_config(self, shop_config):
        return True

    def get_shop_name(self):
        return self.config['info'][0]['name']

    def start_trigger(self, device_id):
        ee.emit(ShopEvents.TRIGGER_DEVICE_START_REQUEST, device_id)
    
    def start_tool(self, tool):
        ee.emit(ShopEvents.TOOL_START_REQUEST, tool)

class ShopEvents():
    TRIGGER_DEVICE_START_REQUEST = "TRIGGER_DEVICE_START_REQUEST" # used to directly start a trigger device
    TRIGGER_DEVICE_STARTED = "TRIGGER_DEVICE_STARTED" # issued by a trigger device when it has started
    TOOL_START_REQUEST = "TOOL_START_REQUEST" # used to directly start a tool
    TOOL_STARTED = "DEVICE_TRIGGERED" # issued by a tool when it has started 
    TOOL_STOP_REQUEST = "TOOL_STOP_REQUEST" # used to directly stop a tool
    TOOL_STOPPED = "TOOL_STOPPED" # issued by a tool when it has stopped
    LISTENER_DEVICE_START_REQUEST = "LISTENER_DEVICE_START_REQUEST" # used to directly start a listener device
    LISTENER_DEVICE_STARTED = "LISTENER_DEVICE_STARTED" # issued by a listener device when it has started
    LISTENER_DEVICE_STOP_REQUEST = "LISTENER_DEVICE_STOP_REQUEST" # used to directly stop a listener device
    LISTENER_DEVICE_STOPPED = "LISTENER_DEVICE_STOPPED" # issued by a listener device when it has stopped
