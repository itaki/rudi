import logging

class ToolManager():

    tools = []

    def addTool(self, tool):
        self.tools.append(Tool(tool['id'], tool['device_links']['triggers'], tool['device_links']['listeners']))
        logging.debug("Tool added: " + tool['id'])

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
    
    id = ""
    triggers = []
    listeners = []

    def __init__(self, id, triggers, listeners):
        self.id = id
        self.triggers = triggers
        self.listeners = listeners