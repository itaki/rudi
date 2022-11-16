import logging
from enum import Enum
import webbrowser
from pymitter import EventEmitter
from . import device
from . import tool
import asyncio
import time
#from websockets import connect


class EventManager():

    ee = EventEmitter()    

    def subscribe(self, listen_to, listen_for, callback):

        global_event = listen_to + "." + listen_for
        self.ee.on(global_event, callback)
        logging.debug("Event Subscription Created: when " + global_event + " is heard, " + callback + " will be called")

        # asyncio.run(hello("ws://rudi-admin:8080"))
    
    def emit(self, source, event, payload):

        global_event = source + "." + event
        self.ee.emit(global_event, payload)
        logging.debug("Event Emitted: " + global_event)

        # asyncio.run(hello("ws://rudi-admin:8080"))

    #async def hello(uri):
    #    async with connect(uri) as websocket:
    #        await websocket.send("Hello from Rudi App!")
    #        await websocket.recv()

    
