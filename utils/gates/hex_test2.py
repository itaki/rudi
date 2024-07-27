import json
from adafruit_servokit import ServoKit
import os

GATES_FILE = "gates.json"
BACKUP_DIR = "_BU"

def get_full_path(filename):
    '''This gets a file associated in the working directory no matter where you run it.
        Useful for VSCode where the terminal doesn't always reside in the directory you are working out of.
        REQUIRES --- 
        from os.path import dirname, join

    '''
    current_dir = os.path.dirname(__file__)  # get current working directory
    full_path = os.path.join(current_dir, f"{filename}")  # set file path
    return(full_path)

# Function to convert hex string to integer
def hex_to_int(hex_str):
    return int(hex_str, 16)

class Gate:
    def __init__(self, gate):
        self.name = gate.name
        self.address = hex_to_int(gate.io_location.address)
        self.pin = gate.io_location.pin
        self.min = gate.min
        self.max = gate.max
        self.status = gate.status
        self.servo = None

    def set_servo(self):
        try:
            self.servo = ServoKit(channels=16, address=self.address).servo[self.pin]
            return True
        except Exception as e:
            print(f"FAILED to create gate at address {self.address} on pin {self.pin}: {e}")
            return False
        
    def open(self):
        self.servo.angle = self.max
        self.status = "open"

class Gate_Manager:
    def __init__(self, gates_file="gates.json", backup_dir="_BU"):
        self.gates_file = gates_file
        self.backup_dir = backup_dir
        self.gates = {}
        self.load_gates()

    def load_gates(self):
        '''Loads gates from a JSON file'''
        path_to_gates_file = get_full_path(self.gates_file)
        if os.path.exists(path_to_gates_file):
            print(f"Loading gates from {path_to_gates_file}")
            with open(path_to_gates_file, 'r') as f:
                self.gates_dict = json.load(f)
            self.build_gates()
        else:
            self.gates_dict = {}
            print('No gate file available')

    def build_gates(self):
        '''Builds Gate objects from the loaded gate data'''
        self.gates = {}
        for gate in self.gates_dict['gates']:
            name = gate['name']
            address = hex_to_int(gate['io_location']['address'])
            pin = gate['io_location']['pin']
            min_pulse = gate['min']
            max_pulse = gate['max']
            
            # Create ServoKit object
            kit = ServoKit(channels=16, address=address)
            kit.servo[pin].set_pulse_width_range(min_pulse, max_pulse)
            
            # Store the servo object in the dictionary
            servos[name] = kit.servo[pin]




# Initialize a dictionary to hold the servo objects
servos = {}

# Load JSON data
gm = Gate_Manager(GATES_FILE, BACKUP_DIR)

print(gm.gates_dict)

