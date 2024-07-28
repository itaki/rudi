import json
from adafruit_servokit import ServoKit
import os
import time

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
    def __init__(self, name, gate_info):
        self.name = name
        self.address = hex_to_int(gate_info['io_location']['address'])
        self.pin = gate_info['io_location']['pin']
        self.min = gate_info['min']
        self.max = gate_info['max']
        self.status = gate_info['status']
        self.init_servo()

    def init_servo(self):
        try:
            self.servo = ServoKit(channels=16, address=self.address).servo[self.pin]
            return True
        except Exception as e:
            print(f"FAILED to create gate at address {self.address} on pin {self.pin}: {e}")
            return False
        
    def open(self):
        self.servo.angle = self.max
        self.status = "open"
        print(f"Gate {self.name} opened.")
    
    def close(self):
        self.servo.angle = self.min
        self.status = "closed"
        print(f"Gate {self.name} closed.")
    
    def identify(self):
        i = 0
        while i < 20:
            self.servo.angle = 80
            time.sleep(.2)
            self.servo.angle = 100
            time.sleep(.2)
            i += 1
        if self.status == 'open':
            self.open()
        else:
            self.close()

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
        for name, gate_info in self.gates_dict['gates'].items():
            self.gates[name] = Gate(name, gate_info)
            print(f'Gate {name} created with address {gate_info["io_location"]["address"]} and pin {gate_info["io_location"]["pin"]}')

    def open_all_gates(self):
        '''Open all gates'''
        for gate in self.gates.values():
            gate.open()

    def close_all_gates(self):
        '''Close all gates'''
        for gate in self.gates.values():
            gate.close()

    def open_gate(self, name):
        '''Open a single gate by name'''
        if name in self.gates:
            self.gates[name].open()
        else:
            print(f"Gate {name} not found.")

    def close_gate(self, name):
        '''Close a single gate by name'''
        if name in self.gates:
            self.gates[name].close()
        else:
            print(f"Gate {name} not found.")

# Load JSON data
if __name__ == "__main__":
    m = Gate_Manager(GATES_FILE, BACKUP_DIR)


