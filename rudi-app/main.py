import os
import logging
import json
from rudi import shop as shop

CONFIG = 'config.json'
HARDWARE = 'hardware.json'

# Determine the directory where main.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Specify the location of config.json based on the current directory
config_path = os.path.join(current_dir, CONFIG)
hardware_path = os.path.join(current_dir, HARDWARE)

# set logging level
#LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
logging.basicConfig(level=LOG_LEVEL)

# load config
with open(config_path) as config_file:
    config = json.load(config_file)

# load hardware database
with open(hardware_path) as hardware_file:
    hardware = json.load(hardware_file)

# start the shop!
shop1 = shop.Shop(config, hardware)


# logging.debug("Simulating left-miter-saw-button being pressed")
# shop.em.emit('left-miter-saw-button', 'PRESSED', {})


while True:
    pass
