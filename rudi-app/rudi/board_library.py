import logging
from rudi.board import Board as RudiBoard
import adafruit_pca9685
from adafruit_servokit import ServoKit
from . import shop
import threading

## DO: Use self.config dictionary object to access device config data
## DON'T Override __init__(), use on_init() instead as needed (and if you declare on_init make sure to emit the ready event)

class ServoHat(RudiBoard):

    def on_init(self):
        #register my valid events in case anyone asks what I can do
        self.register_event("CREATED")

        board = ServoKit(channels=self.config['channels'], address=hex(int(self.config['address'], 16)) )

        self.emit_event("CREATED", {})

    def on_press(btn): 
        btn.self.emit_event("PRESSED", {})




