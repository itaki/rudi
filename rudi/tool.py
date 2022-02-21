import logging
import pickle
from . import shop as shop

class ToolManager():

    tools = []

    def addTool(self, tool_config):
        #self.tools.append(Tool(tool['id'], tool['device_links']['triggers'], tool['device_links']['listeners']))
        self.tools.append(Tool(tool_config))

    def addTools(self, tools):
        for tool in tools:
            self.addTool(tool)

    def removeToolById(self, id):
        # may need to convert tools collection to dict in order to do this without looping through all list items
        logging.debug("Removing device: " + id)

    def removeAllTools(self):
        self.tools = []
        logging.debug("All tools removed!")

    def printToolList(self):
        print("\n" + "TOOLS:" + "\n" + "===================================")
        for tool in self.tools:
            print("\"" + tool.id + "\"")

            output = "    Triggers: "
            for trigger in tool.triggers:
                output = output + "\n        \"" + trigger['id'] + "\""
            print(output)

            output = "    Listeners: "
            for listener in tool.listeners:
                output = output + "\n        \"" + listener['id'] + "\""
            print(output + "\n")



class Tool():
    
    config = {}

    def __init__(self, tool_config):
        self.config = tool_config
        shop.ee.on(shop.ShopEvents.TOOL_START_REQUEST, self.request_listener)
        shop.ee.on(shop.ShopEvents.TRIGGER_DEVICE_STARTED, self.trigger_start_listener)
        logging.debug("Tool Added: " + self.config["id"])
    
    def request_listener(self, tool_id):
        # handles direct tool start request events
        if tool_id == self.config["id"]:
            logging.debug(self.config["id"] + " heard tool start request")
            shop.ee.emit(shop.ShopEvents.TOOL_STARTED, pickle.dumps(self.config))
    
    def trigger_start_listener(self, trigger_id):
        # handles trigger device start events
        if trigger_id in self.config["device_links"]["triggers"]:
            logging.debug(self.config["id"] + " heard trigger start of: " + trigger_id)
            shop.ee.emit(shop.ShopEvents.TOOL_STARTED, pickle.dumps(self.config))