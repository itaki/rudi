import os
import logging
import json
from rudi import shop as shop

# set logging level
#LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
logging.basicConfig(level=LOG_LEVEL)

# load config
with open('config.json') as config_file:
    config = json.load(config_file)

# load hardware database
with open('hardware.json') as hardware_file:
    hardware = json.load(hardware_file)

# start the shop!
shop1 = shop.Shop(config, hardware)


# logging.debug("Simulating left-miter-saw-button being pressed")
# shop.em.emit('left-miter-saw-button', 'PRESSED', {})


while True:
    pass
