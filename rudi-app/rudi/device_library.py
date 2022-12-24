import logging
from rudi.device import Device as RudiDevice
from . import shop
from gpiozero import Device, Button, LED
from sshkeyboard import listen_keyboard
import threading

## DO: Use self.config dictionary object to access device config data
## DON'T Override __init__(), use on_init() instead as needed (and if you declare on_init make sure to emit the ready event)


class Keyboard(RudiDevice):
    
    thread = None
    key_map = {}

    def on_init(self):

        # register my valid events in case anyone asks what I can do
        # note: we do not register the dynamic events defined in the preferences
        self.register_event("KEY_PRESSED")

        # create a mapping of keys to instance id b/c python callback with threading gets weird
        for mapping in self.config['preferences']["mappings"] :
            if mapping['keyboard_key'] in Keyboard.key_map :
                logging.warn(f"Ignoring { self.config['id'] }'s request to map { mapping['keyboard_key'] } to { mapping['event_name'] } because that key was already mapped by { Keyboard.key_map[mapping['keyboard_key']]['source_instance'] } to { Keyboard.key_map[mapping['keyboard_key']]['event_name'] }")
            else :
                key_meta = {}
                key_meta['event_name'] = mapping['event_name']
                key_meta['source_instance'] = self.config['id']  # we need to store the current instance id b/c 'self' can't be trusted past this point
                Keyboard.key_map.update({
                    mapping['keyboard_key'] : key_meta
                })

        # start keyboard listener on new thread
        def on_press(key):
            Keyboard.handle_on_press(key)
        def start_listener():
            listen_keyboard(on_press=on_press)
        if (Keyboard.thread == None):
            logging.debug("starting new thread for keyboard listener")
            Keyboard.thread = threading.Thread(target=start_listener)
            Keyboard.thread.start()

        self.emit_event("READY", {})
    
    @staticmethod
    def handle_on_press(pressed_key):
        logging.debug("Handling key " + pressed_key)
        if pressed_key in Keyboard.key_map :
        #for key, meta in Keyboard.key_map.items(): 
            #if key == pressed_key:
            # we can't use 'self' here to get the source so we use the instance value we stored earlier
            shop.em.emit(
                Keyboard.key_map[pressed_key]['source_instance'],
                Keyboard.key_map[pressed_key]['event_name'],
                {'pressed_key': pressed_key}
            )

class SimpleButton(RudiDevice):

    def on_init(self):
        #register my valid events in case anyone asks what I can do
        self.register_event("PRESSED")

        Button.self = ''
        button = Button(self.config['connection']['pin'])
        button.self = self
        button.when_pressed = self.on_press.__func__

        self.emit_event("READY", {})

    def on_press(btn): 
        btn.self.emit_event("PRESSED", {})




class Gpio_Shop_Light(RudiDevice):
    '''This is a simple LED which can be on, off, toggled, forced off, delayed off, and blink delayed off

        Default is simple on and off.
        Add preferences to config.json for options
        "preferences" : {
                "turn_off_delay" : 3,
                "delay_style" : "SOLID"
                "blink_time" : ".5"
            },
        delay is in seconds
        style options are "BLINK" and "SOLID" but if left blank defaults to "SOLID"
    '''

    def on_init(self):
        #register events that I can broadcast to the world
        self.register_event("TURNED_ON")
        self.register_event("TURNED_OFF")
        self.register_event("BEGAN_DELAYED_TURN_OFF")

        #register actions that I can do
        self.register_action("TURN_ON", self.handle_turn_on_action)
        self.register_action("TURN_OFF", self.handle_turn_off_action)
        self.register_action("TOGGLE", self.handle_toggle_action)
        self.register_action("FORCE_OFF", self.handle_force_off_action)
        
        #create GPIOZERO LED on proper pin
        self.light = LED(self.config['connection']['pin'])

        # set state vars
        self.state = "OFF" # can also be ON or SHUTTING_DOWN

        # set preferences
        self.turn_off_delay = 0
        self.blink_time = .5
        self.delay_style = "SOLID" # can also be BLINK
        if 'turn_off_delay' in self.config['preferences'] :
            self.turn_off_delay = self.config['preferences']['turn_off_delay']
        if 'delay_style' in self.config['preferences'] :
            self.delay_style = self.config['preferences']['delay_style']
        if 'blink_time' in self.config['preferences'] :
            self.blink_time = float(self.config['preferences']['blink_time'])

        #make a blank list to keep modifiers
        self.devices_who_want_me_on = []

        #tell the world I'm ready aka "hello world"
        self.emit_event("READY", {})

    #make action handlers to spawn off functions
    def handle_turn_on_action(self, payload) :
        self.turn_on(payload)
    def handle_turn_off_action(self, payload) :
        self.turn_off(payload)
    def handle_toggle_action(self, payload) :
        self.toggle(payload)
    def handle_force_off_action(self, payload) :
        self.force_off()

    #all my methods
    def turn_on(self, payload) :
        if payload['source'] not in self.devices_who_want_me_on:
            self.devices_who_want_me_on.append(payload['source'])
        if self.state == "SHUTTING_DOWN" :
            self.kill_shutdown_timer()
        if self.state != "ON" :
            logging.debug(f"TURNING ON {self.config['label']}")
            self.light.on()
            self.state = "ON"
            self.emit_event("TURNED_ON", {})
    
    def turn_off(self, payload) :
        if payload['source'] in self.devices_who_want_me_on : # off requests are only valid if the requesting device is in this list
            self.devices_who_want_me_on.remove(payload['source'])
            if self.state == "ON" :
                if len(self.devices_who_want_me_on) > 0 : #check to see if any other devices want me on
                   logging.debug(f"{self.config['id']} received a turn off request from {payload['source']} and removed {payload['source']} from the 'devices_who_want_me_on' list but {self.config['id']} will stay on for: {self.devices_who_want_me_on}")
                else:            
                    if self.turn_off_delay > 0 :
                        if self.delay_style == "BLINK" :
                            self.light.blink(self.blink_time, self.blink_time, None, True)
                        self.timer = threading.Timer(self.turn_off_delay, self.force_off) 
                        self.timer.start()
                        logging.debug(f"TURNING OFF {self.config['label']} IN {self.turn_off_delay} SECONDS")
                        self.state = "SHUTTING_DOWN"
       
                    else :
                        self.force_off()
    
    def force_off(self) :
        if self.state == "SHUTTING_DOWN" :
            self.kill_shutdown_timer()
        if self.state != "OFF" :
            self.devices_who_want_me_on.clear() #  empties the devices_who_want_me_on list
            logging.debug(f"TURNING OFF {self.config['label']}")
            self.light.off()
            self.state = "OFF"
            self.emit_event("TURNED_OFF", {})
             
    def toggle(self, payload):
        #this toggles visual state
        logging.debug(f"TOGGLING {self.config['label']}")
        if self.state == "ON" and payload['source'] in self.devices_who_want_me_on:
            self.turn_off(payload)
        else: # if I'm off, shutting down, or a new device is requesting me to be on
            self.turn_on(payload)

    def kill_shutdown_timer(self):
        #timer is only used for delaying turn off
        # just kills the timer if it's running
        try:
            self.timer.cancel()
        except:
            pass
        logging.debug(f"Timer cancelled for {self.config['label']} ")


class SuperSimpleLedLight(RudiDevice):

    # I am a STATELESS LED light device - I always do the last thing asked of me
    # I am not very practical for real world applications

    def on_init(self):
        self.register_event("TURNED_ON")
        self.register_event("TURNED_OFF")

        self.register_action("TURN_ON", self.turn_on_light)
        self.register_action("TURN_OFF", self.turn_off_light)

        self.light = LED(self.config['connection']['pin'])

        self.emit_event("READY", {})
    
    def turn_on_light(self, event) :
        self.light.on()
        self.emit_event("TURNED_ON", {})
    
    def turn_off_light(self, event) :
        self.light.off()
        self.emit_event("TURNED_OFF", {})

class VoltageDetector(RudiDevice):
    
    # needs more work

    baseline_voltage = 0
    sensitivity = 0

    def on_init(self):

        self.register_event("TOOL_STARTED")
        self.register_event("TOOL_STOPPED")
        self.register_event("TOOL_CHANGED")

        # add code here to setup hardware connection
        # GPIO.whatever(self.config.connection.whatever)

        # collect a series of readings and set the proper baseline and sensitivity
        # self.baseline_voltage = 1000
        # self.sensitivity = 200

        self.monitor_voltage()

        self.emit_event("READY", {})
    

    def monitor_voltage(self) :
        
        # poll GPIO for voltage readings continually
        logging.info(self.config["label"] + " is watching for voltage changes")

        # if logic decides the tool started:
        # self.emit_event("TOOL_STARTED", {})
        # self.emit_event("TOOL_CHANGED", {})

        # if logic decides the tool stopped:
        # self.emit_event("STOPPED", {})
        # self.emit_event("TOOL_CHANGED", {})
    


class DustCollector(RudiDevice):

    minimum_runtime_minutes = 10

    def on_init(self):

        self.register_event("STARTED")
        self.register_event("STOPPED")

        self.register_action("START", "start_dust_collector")
        self.register_action("STOP", "stop_dust_collector")

        if "minimum_runtime_minutes" in self.config["preferences"]:
            self.minimum_runtime_minutes = self.config["preferences"]["minimum_runtime_minutes"]

        # add code here to setup hardware connection
        # GPIO.whatever(self.config.connection.whatever)

        self.emit_event("READY", {})
    
    def start_dust_collector(self) :
        # add code here to tell GPIO to start the dust collector
        self.emit_event("STARTED", {})


    def stop_dust_collector(self) :
        # add code here to tell GPIO to stop the dust collector
        self.emit_event("STOPPED", {})
    

class Gate(RudiDevice):

    open_pwm = 0
    closed_pwm = 0

    def on_init(self):

        self.register_event("OPENED")
        self.register_event("CLOSED")
        self.register_event("CHANGED")

        self.register_action("OPEN", "open_gate")
        self.register_action("CLOSE", "close_gate")

        if "open_pwm" in self.config["preferences"]:
            self.open_pwm = self.config["preferences"]["open_pwm"]
            logging.info("Setting open_pwm for " + self.config["label"] + " to " + self.open_pwm)
        
        if "closed_pwm" in self.config["preferences"]:
            self.closed_pwm = self.config["preferences"]["closed_pwm"]
            logging.info("Setting closed_pwm for " + self.config["label"] + " to " + self.closed_pwm)
        
        # add code here to setup hardware connection
        # GPIO.whatever(self.config.connection.whatever)

        self.emit_event("READY", {})
    
    def open_gate(self):
        logging.info("Opening gate " + self.config["id"])
        
        # Add code to talk GPIO and tell it to go to the open_pwm setting
        # if successful:
        self.emit_event("OPENED", {})
        self.emit_event("CHANGED", {})
    
    def close_gate(self):
        logging.info("Closing gate " + self.config["id"])
        
        # Add code to talk GPIO and tell it to go to the closed_pwm setting
        # if successful:
        self.emit_event("CLOSED", {})
        self.emit_event("CHANGED", {})