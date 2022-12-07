import os
import logging
import json
from rudi import shop as shop

# set logging level
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
logging.basicConfig(level=LOG_LEVEL)

# load config
with open('config.json') as json_file:
    config = json.load(json_file)

# start the shop!
shop1 = shop.Shop(config)


# logging.debug("Simulating left-miter-saw-button being pressed")
# shop.em.emit('left-miter-saw-button', 'PRESSED', {})


while True:
    pass
