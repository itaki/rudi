import os
import logging
import json
from rudi import shop as shop

# load config
with open('config.json') as json_file:
    config = json.load(json_file)

# validate config file before trying to set logging level
if not shop.Shop.validate_config(shop, config):
    quit()
else:
    # # set logging level
    LOG_LEVEL = config['env'][0]['logging_level']
    # LOG_LEVEL = os.environ.get('LOG_LEVEL', 'WARNING')
    logging.basicConfig(level=LOG_LEVEL)

    # start the shop!
    shop1 = shop.Shop()
    shop1.loadConfig(config)



