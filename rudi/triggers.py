import logging
from rudi.device import TriggerDevice

#### Add custom trigger devices below!


class VoltageDetector(TriggerDevice):

    base_voltage = 10