import os
import logging
import json
from rudi import shop as shop

# set logging level
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING')
logging.basicConfig(level=LOG_LEVEL)

# load config
with open('config.json') as json_file:
    config = json.load(json_file)

# start the shop!
shop1 = shop.Shop(config)

# manually start a trigger
shop1.start_trigger("table-saw-voltage-detector")

# manually start a tool
#shop1.startTool("table-saw-middle")


