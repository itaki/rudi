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

    def subscribe(self, event, action):

        self.ee.on(event, action)

        # asyncio.run(hello("ws://rudi-admin:8080"))
    
    def emit(self, event, source, payload):

        self.ee.emit(event, source, payload)

        # asyncio.run(hello("ws://rudi-admin:8080"))

    #async def hello(uri):
    #    async with connect(uri) as websocket:
    #        await websocket.send("Hello from Rudi App!")
    #        await websocket.recv()

    
