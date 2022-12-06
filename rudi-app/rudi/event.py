import logging
from pymitter import EventEmitter
import webbrowser
import asyncio
import time
#from websockets import connect


class EventManager():

    ee = EventEmitter()    

    def subscribe(self, listen_to, listen_for, callback):

        global_event = listen_to + "." + listen_for
        logging.debug(f"Event subscription created: for {global_event}")
        self.ee.on(global_event, callback)
        

        # asyncio.run(hello("ws://rudi-admin:8080"))
    
    def emit(self, source, event, payload):

        global_event = source + "." + event
        logging.debug(f"Event emitted: {global_event}")
        self.ee.emit(global_event, payload)
        

        # asyncio.run(hello("ws://rudi-admin:8080"))

    #async def hello(uri):
    #    async with connect(uri) as websocket:
    #        await websocket.send("Hello from Rudi App!")
    #        await websocket.recv()

    
