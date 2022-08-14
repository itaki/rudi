import logging
import pickle
from . import shop as shop

class ToolManager():

    tools = []

    def add_tool(self, tool_config):
        #self.tools.append(Tool(tool['id'], tool['device_links']['triggers'], tool['device_links']['listeners']))
        self.tools.append(Tool(tool_config))

    def add_tools(self, tools):
        for tool in tools:
            self.add_tool(tool)

    def remove_tool_by_id(self, id):
        # may need to convert tools collection to dict in order to do this without looping through all list items
        logging.info("Removing device: " + id)

    def remove_all_tools(self):
        self.tools = []
        logging.info("All tools removed!")

    def print_tool_list(self):
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
        logging.info("Tool Added: " + self.config["id"])
    
    def request_listener(self, tool_id):
        # handles direct tool start request events
        if tool_id == self.config["id"]:
            logging.info(self.config["id"] + " heard tool start request")
            shop.ee.emit(shop.ShopEvents.TOOL_STARTED, pickle.dumps(self.config))
    
    def trigger_start_listener(self, trigger_id):
        # handles trigger device start events
        if trigger_id in self.config["device_links"]["triggers"]:
            logging.info(self.config["id"] + " heard trigger start of: " + trigger_id)
            shop.ee.emit(shop.ShopEvents.TOOL_STARTED, pickle.dumps(self.config))