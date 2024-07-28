import curses
import time
import os, sys

import questionary as q
import blinky_bits as bb
import reorder_dict
from pathlib import Path
from adafruit_servokit import ServoKit
from gpiozero import LED, RGBLED, Button


from styles import custom_style_dope, get_styles


style = custom_style_dope
import board
import busio
import json
import get_full_path
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
### hat = adafruit_pca9685.PCA9685(i2c) Put this in the application
GATES_FILE = "gates.json"
BACKUP_DIR = "_BU"
class Gate_Manager:
    gates: dict  # dictionary of gate objects
    gates_file: str
    changed = False
    backed_up = False

    def __init__(self, gates_file="gates.json", backup_dir="_BU") -> None:
        self.gates_file = gates_file
        self.load_gates()  # load the gates from the file retuns
        self.backup_dir = backup_dir

    def load_gates(self):
        '''Takes a JSON file and returns a dictionary'''
        # LOAD ALL THE GATES
        if os.path.exists(self.gates_file):  # if there is a gates file load it
            file_path = get_full_path.path(self.gates_file)  # set the file path
            with open(file_path, 'r') as f:  # read the gate json file
                self.gates_dict = json.load(f)  # load the json into a python dict called gates_dict
            self.build_gates()  # builds the gate objects from the gates_dict
        else:
            self.gates_dict = {}  # no gates
            print('no gate file available')  # Fix this in future versions with get_gates

    def build_gates(self):
        '''Builds objects from the gate_list. Will not add gate if address doesn't exist'''
        self.gates = {}  # temporary variable to hold the gates

        for gate in self.gates_dict:  # create gate object
            # print (gate)
            self.gates[gate['name']] = Gate(
                gate['name'],
                gate['id'],
                gate['physical_location'],
                gate['status'],
                gate['io_location'],
                gate['min'],
                gate['max'],
                gate['info']
            )
            if self.gates[gate['name']].set_servo():  # if it can set a servo, meaning the address is valid at gate
                print(f"✅ SUCCESS {gate} ")
            else:
                print(f"❌ REMOVED {gate} ")
                self.gates.pop(gate['name'])

    def select_gates_file(self):
        files = os.listdir(self.backup_dir)
        files.append("Keep Files")
        files.reverse()
        #print (files)
        selected_file = q.select("Which file would you like to restore? Top is newest",
                    choices = files, 
                    default=None, 
                    qmark='?', 
                    pointer='»', 
                    style=style, 
                    use_shortcuts=False, 
                    use_arrow_keys=True, 
                    use_indicator=True, 
                    use_jk_keys=True, 
                    show_selected=True, 
                    instruction=None,).ask()
        
        return selected_file

    def write_gates(self, note = ''):
        '''Writes the gates in memory to the gates_file. Makes a backup beforehand'''
        # Backup current file
        bb.backup_file(self.gates_file, note)
        # create the file path
        file_path = get_full_path.path(self.gates_file)  # set the file path
        #convert the gates object to a format that can be written by json
        new_gates_file = []
        new_gates_list = list(self.gates.values())
        for g in new_gates_list:
            new_gates_file.append(g.__dict__)
        with open(file_path, 'w') as f:  # 'w' writes over the whole file
            f.write(json.dumps(new_gates_file, indent = 4))
            print(f"New gates written to {file_path}")
    
    def view_gates(self):
        if self.gates == False:
            if q.confirm("There are no gates, would you like to load some gates?", style=style).ask:
                self.load_gates()
                return True
        else:
            for gate in self.gates:
                s_gate = self.gates[gate]
                print(s_gate.__dict__)
            return False
    
    def view_gates_compact(self):
        if self.gates == False:
            if q.confirm("There are no gates, would you like to load some gates?", style=style).ask:
                self.load_gates()
                return True
        else:
            for gate in self.gates:
                s_gate = self.gates[gate]
                print (f"Gate {s_gate.name} at {s_gate.physical_location} on pin {s_gate.io_location['pin']} min:{s_gate.min} | max:{s_gate.max} -- {s_gate.info}")
            return False
                
    def clear_gates(self):
        action = q.confirm(f"ARE YOU SURE YOU WANT TO CLEAR ALL GATES?", style=style).ask()
        
        if action:
            self.gates = {}
            return True
        return False

    def set_gate_name(self, gate_key):
        my_gate = self.gates[gate_key]
        #ask about the current name and renaming it
        print(f"Current name is {my_gate.name}")
        print("Depending on the size of the gate button, the name should be very short. One to 3 charaters.")
        new_name = q.text("What name would you like to use?", style = style).ask()
        if new_name == '':
            print("Can't be empty, please give your gate a name")
            self.set_gate_name(gate_key)
        if new_name == 'new':
            print("Cannon use 'new' as name, please choose another?")
            self.set_gate_name(gate_key)
        # for all the g's in gates check to see if it's the same name
        for g in self.gates:
            s_gate = self.gates[g] # note that in this case, 'gate' alone is also the name of the key that is paired with the object
            if new_name == g != gate_key:
                print(f"That name alread taken by the gate at loaction {s_gate.location} on pin {s_gate.pin}")
                self.set_gate_name(gate_key)
            #first change the key  
            #https://stackoverflow.com/questions/16475384/rename-a-dictionary-key
            print(f"Saving gate {my_gate.name} as {new_name}")
            new_gates = {new_name if k == my_gate.name else k:v for k,v in self.gates.items() }
            self.gates = new_gates
            #now change the name since we know the key value for it 
            self.gates[new_name].name = new_name
            return True
            
        else:
            return False

    def set_gate_pin(self, gate_key):
        my_gate = self.gates[gate_key]
        # get requested pin
        print(f"Gate is currently listed as {my_gate['pin']}")
        requested_pin = int(q.text("What pin is the gate on? (0 - 15)", style = style).ask())
        if 0 <= requested_pin <= 15:
            if len(self.gates) != 0:
                for g in self.gates:
                    s_gate = self.gates[g]
                    if requested_pin == s_gate.pin and requested_pin != my_gate['pin']:
                        print(f"{requested_pin} already used by gate {s_gate.name} at {s_gate.location}. Double check your gates. 'q' to quit.") 
                        self.set_gate_pin(gate_key)
            self.gates[gate_key].pin = int(requested_pin)
            return True
            
        elif requested_pin == 'q':
            return False
        else:
            print(f"{requested_pin} not a pin number. 'q' to quit without setting pin")

    def rattle_gate(self, stdscr, gate_key):
        ''' CURSES function so needs wrapping, takes gate_key, moves gate around until quit'''
        my_gate = self.gates[gate_key]
        # get size of terminal canvas
        height, width = stdscr.getmaxyx()
        styles = get_styles()
        stdscr.clear()
        stdscr.nodelay(True)

        #create the strings
        info = f"Currently identifying GATE {my_gate.name} at {my_gate.physical_location}"
        instructions = "'q' to quit"
        #calculate position
        info_x = bb.center_x(width, info)
        info_y = int((height // 2) - 1)
        instructions_x = bb.center_x(width, instructions)
        instructions_y = int((height // 2) + 1)
        cent_x = int(width // 2)
        cent_y = int(height // 2)
        # print to screen
        stdscr.addstr(info_y, info_x, info, styles['heading'])
        stdscr.addstr(instructions_y, instructions_x, instructions, styles['warning'])
        angle = 70
        increase = True
        key = None
        while True:
            try:
                key = stdscr.getkey()
            except:
                key = None
            if key == None:
                #stdscr.addstr("It's working")
                if increase == True:
                    angle = angle + 1
                    my_gate.servo.angle = angle
                    if angle >= 110:
                        increase = False
                else:
                    angle = angle - 1
                    my_gate.servo.angle = angle
                    if angle <= 70:
                        increase = True
                stdscr.addstr(cent_y, cent_x, str(angle))
                time.sleep(.02)
            if key == 'q':
                return True

            stdscr.refresh()
    
    def identify_gate(self, gate_key):
        '''takes gate_key and packages it in a wrapper to ship off to rattle_gate()'''
        my_gate = self.gates[gate_key]
        #print (f"Indentifying gate {my_gate.name} at {my_gate.location}")
        curses.wrapper(self.rattle_gate, gate_key)
        return True
    
    def set_location(self, gate_key):
        my_gate = self.gates[gate_key]
        print(f"Current location is {my_gate.location}")
        new_location = q.text("What is the location of this gate? 'q' to leave as is", style = style).ask()
        if new_location != 'q':
            self.gates[gate_key].location = new_location
            return True
        elif new_location != None:
            return True
        else:
            print (f"You must provide a location")
            self.set_location(gate_key)
    
    def set_all_gates_angles(self):
        for g in self.gates:
            if not self.set_min(g):
                return False
            if not self.set_max(g):
                return False
        return True

    def set_gate_angle(self, stdscr, gate_key, side):
        """ CURSES function so needs wrapping, create interface to adjust the gate"""

        my_gate = self.gates[gate_key]
        pin = my_gate.io_location['pin']
        key = None
        adjustment = 0
        flagged = True

        too_high = False
        too_low = False
        
        current_min = my_gate.min
        current_max = my_gate.max
        if side == 'min':
            angle = current_min
        else:
            angle = current_max

        rows_of_info = 8
        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Add no echo
        curses.noecho()
        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Initialization
        height, width = stdscr.getmaxyx()
        start_y = int((height // 2) - (rows_of_info // 2))
        cent_x = int(width // 2)

        while True:
            # Set the adjustment for each key pressed
            if key == "KEY_DOWN":
                adjustment = -1
            elif key == "KEY_LEFT":
                adjustment = -10
            elif key == "KEY_UP":
                adjustment = 1
            elif key == "KEY_RIGHT":
                adjustment = 10
            elif key == "q":
                return -1
            elif key == "s":
                return int(angle)
            elif key is None:
                flagged = True
            if adjustment != 0 or flagged:
                flagged = False
                angle += adjustment   
                adjustment = 0  
                if angle > 180:
                    too_high = True
                    angle = 180
                elif angle < 0: 
                    too_low = True
                    angle = 0
                else:
                    too_high = False
                    too_low = False
                
                print(f"Angle = {angle}")
                my_gate.servo.angle = angle

            # Declaration of strings
            title = f"Set {side} for gate {my_gate.name} at {my_gate.physical_location} on pin {my_gate.io_location['pin']}"[:width-1]
            instructions = "Use arrow keys  :  '0' to recenter  :  'q' to quit  :  's' to save"[:width-1]
            angle_reading = f"Angle: {angle}"[:width-1]
            if too_low:
                angle_reading += ' WARNING!!! TOO LOW'
            if too_high:
                angle_reading += ' WARNING!!! TOO HIGH'
            statusbarstr = f"Press 'q' to exit | Press 's' to save | Last key pressed: {key}"[:width-1]

            # Centering calculations
            start_x_title = bb.center_x(width, title)
            start_x_instructions = bb.center_x(width, instructions)
            start_x_angle_reading = bb.center_x(width, angle_reading)
            min_marker = cent_x + (my_gate.min - 90)
            max_marker = cent_x + (my_gate.max - 90)
            angle_marker = cent_x + (angle - 90)

            # Clear the screen
            stdscr.clear()

            # Render status bar
            stdscr.attron(curses.color_pair(3))
            statusbarstr = statusbarstr[:width-1]  # Truncate status bar string to fit terminal width
            stdscr.addstr(height-1, 0, statusbarstr)
            stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
            stdscr.attroff(curses.color_pair(3))

            # Render the title
            stdscr.addstr(start_y, start_x_title, title, curses.color_pair(2) | curses.A_BOLD)
            # Render the instructions
            stdscr.addstr(start_y + 2, start_x_instructions, instructions)
            
            # Render the min marker 
            min_color = curses.color_pair(2) if side == 'min' else curses.color_pair(1)
            max_color = curses.color_pair(2) if side == 'max' else curses.color_pair(1)

            stdscr.addstr(start_y + 3, min_marker, '|', min_color | curses.A_BOLD)
            stdscr.addstr(start_y + 3, max_marker, '|', max_color | curses.A_BOLD)
            # Render the current angle marker gauge
            stdscr.addstr(start_y + 3, angle_marker, '|')
            # Render the angle gauge
            stdscr.addstr(start_y + 4, (width // 2) - 90, '-' * min(180, width-1))  # Ensure it fits in width
            stdscr.addstr(start_y + 5, cent_x - 91, '0', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x - 61, '30', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x - 31, '60', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x - 1, '90', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x + 29, '120', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x + 59, '150', curses.color_pair(1))
            stdscr.addstr(start_y + 5, cent_x + 89, '180', curses.color_pair(1))
            # Render the current values
            stdscr.addstr(start_y + 7, start_x_angle_reading, angle_reading)

            # Refresh the screen
            stdscr.refresh()

            # Wait for next input
            key = stdscr.getkey()



    def set_min(self, gate_key):
        gate_min = curses.wrapper(self.set_gate_angle, gate_key, 'min')
        if gate_min != -1:
            self.gates[gate_key].min = gate_min
            return True
        else:
            print ("Changes abandoned")
            return False
    
    def set_max(self, gate_key):
        gate_max = curses.wrapper(self.set_gate_angle, gate_key, 'max')
        if gate_max != -1:
            self.gates[gate_key].max = gate_max
            return True
        else:
            print ("Changes abandoned")
            return False

    def set_info(self, gate_key):
        my_gate = self.gates[gate_key]
        print(f"Current info is {my_gate.info}")
        new_info = q.text("Infomation about this gate? 'q' to leave as is", style = style).ask()
        self.gates[gate_key].info = new_info
        return True

    def remove_gate(self, gate_key):
        
        if self.delete_gate(gate_key):
            return True
        else:
            return False  

    def delete_gate(self, gate_key, confirm = True):
        my_gate= self.gates[gate_key]
        delete = False
        if confirm == True:
            delete = q.confirm(f"Are you sure you want to remove {my_gate.name} at location {my_gate.location}?", style = style).ask()
        if delete or not confirm:
            self.gates.pop(gate_key)
            return True
        else:
            print (f"Gate {my_gate.name} not removed.")
            return False

    def add_new_gate(self):
        number = len(self.gates)
        new_gate_object = Gate(
            'new',
            number,
            None,
            False,
            None,
            85,
            95,
            'New'
        )
        self.gates.update({'new': new_gate_object})
        self.modify_gate('new')
        
    def modify_gate(self, gate_key):
        if self.set_gate_pin(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_location(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_min(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_max(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_info(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        if self.set_gate_name(gate_key) != True:
            self.delete_gate(gate_key, False)
            return False
        return True

    def select_gate(self):
        gates_list = list(self.gates.keys())
        gates_list.append("Quit")  # Add a Quit option to the list
        gate_key = q.select("Select gate or quit:",
                            choices=gates_list, 
                            default=None, 
                            qmark='?', 
                            pointer='»', 
                            style=style, 
                            use_shortcuts=False, 
                            use_arrow_keys=True, 
                            use_indicator=True, 
                            use_jk_keys=True, 
                            show_selected=True, 
                            instruction=None).ask()
        return gate_key

    
    def open_gate(self, gate_key):
        my_gate = self.gates[gate_key]
        my_gate.open()

    def close_gate(self, gate_key):
        my_gate = self.gates[gate_key]
        my_gate.close()

    def open_gates(self):
        gates_list = list(self.gates.keys())
        for g in gates_list:
            self.open_gate(g)

    def close_gates(self):
        gates_list = list(self.gates.keys())
        for g in gates_list:
            self.close_gate(g)
    
    def set_gates(self, open_gates):
        '''Takes a list of gates that need to be open and opens them while making sure the rest are closed'''
        for g in self.gates:
            current_gate = self.gates[g]
            if current_gate.name in open_gates:
                self.open_gate(g)
                #print(f'OPENING gate {current_gate.name} status = {current_gate.status}')
                
            else:
                self.close_gate(g)
                #print(f'CLOSEING gate {current_gate.name} status = {current_gate.status}')
                
def gate_actions_menu(gm):
    while True:
        gate_key = gm.select_gate()
        if gate_key == "Quit":
            break  # Break the loop to return to the main menu

        action_choices = {
            "Identify gate": gm.identify_gate,
            "Modify gate": gm.modify_gate,
            "Remove gate": gm.remove_gate,
            "Open gate": gm.open_gate,
            "Close gate": gm.close_gate,
            "Set min/max": lambda x: gm.set_gate_angle(x, 'both'),  # Example lambda for setting both
            "Quit to Main Menu": None  # Placeholder for quitting
        }

        print("Select an action for the gate:")
        action = q.select("Choose an action:",
                          choices=list(action_choices.keys()),
                          default=None,
                          qmark='?',
                          pointer='»',
                          style=style,
                          use_shortcuts=True,
                          use_arrow_keys=True,
                          use_indicator=True,
                          use_jk_keys=True,
                          show_selected=True,
                          instruction=None).ask()

        if action == "Quit to Main Menu":
            break

        if action_choices[action]:
            action_choices[action](gate_key)

def main_menu(gm):
    while True:  # This loop will keep running until a break condition is met
        print("---------MAIN MENU----------")
        choices = (
            "view gates : compact",
            "view gates : extended",
            "load gates",
            "clear all gates",
            "add gate",
            "reorder gates",
            "set all gates - min & max",
            "modify gate",
            "remove gate",
            "identify gate",
            "open all gates",
            "close all gates",
            "quit"  # Option to quit
        )
        action = q.select("What do you want to do?",
                          choices=choices,
                          default=None,
                          qmark='?',
                          pointer='»',
                          style=style,
                          use_shortcuts=True,
                          use_arrow_keys=True,
                          use_indicator=True,
                          use_jk_keys=True,
                          show_selected=True,
                          instruction=None).ask()

        if action == "quit":
            print("Exiting program...")
            break  # Exit the loop, which ends the function and thus the program

        elif action == "view gates : compact":
            gm.view_gates_compact()

        elif action == "view gates : extended":
            gm.view_gates()

        elif action == "load gates":
            selected_file = gm.select_gates_file()
            print(f"SELECTED GATES FILE {selected_file}")
            if selected_file != "Keep Files":
                selected_file = BACKUP_DIR + '/' + selected_file
                gm.load_gates(selected_file)
                gm.write_gates('load_from_backup')
            else:
                print("No gates loaded")

        elif action == "clear all gates":
            if gm.clear_gates():
                gm.write_gates('clear_all')
            else:
                print("Gates not cleared")

        elif action == "add gate":
            if gm.add_new_gate():
                print("Gate added")
                gm.write_gates('gate_added')
            else:
                print("Gate not added")

        elif action == "reorder gates":
            reordered_gates = reorder_dict.reorder(gm.gates)
            gm.gates = reordered_gates
            print("Gates reordered")
            gm.view_gates_compact()
            gm.write_gates("reordered")

        elif action == "set all gates - min & max":
            if gm.set_all_gates_angles():
                print("All Gates Set")
            else:
                print("Only a few gates set")
            gm.write_gates('angles_set')

        elif action == 'modify gate' or action == 'remove gate' or action == 'identify gate':
            gate_actions_menu(gm)


        elif action == "open all gates":
            gm.open_gates()

        elif action == "close all gates":
            gm.close_gates()

        # Pause or a visual separator can be helpful for user experience
        input("Press Enter to continue...")


 
class Gate:
    def __init__(self, name, id, physical_location, status, io_location, minimum, maximum, info):
        self.name = name
        self.id = id
        self.physical_location = physical_location
        self.status = status
        self.io_location = io_location
        self.min = minimum
        self.max = maximum
        self.info = info
        self.servo = None

    def set_servo(self):
        try:
            self.servo = ServoKit(channels=16, address=self.io_location['address']).servo[self.io_location['pin']]
            return True
        except Exception as e:
            print(f"FAILED to create gate at address {self.io_location['address']} on pin {self.io_location['pin']}: {e}")
            return False

    def open(self):
        if self.servo:
            self.servo.angle = self.max
            print(f'Opening {self.name}')
            self.status = 0
            #self.stop_pwm()

    def close(self):
        if self.servo:
            self.servo.angle = self.min
            print(f'Closing {self.name}')
            self.status = 1
            #self.stop_pwm()

    def stop_pwm(self):
        if self.servo:
            try:
                self.servo.angle = None  # This stops the PWM signal to the servo
                #print(f'Stopping PWM for {self.name}')
            except Exception as e:
                print(f"Failed to stop PWM for {self.name}: {e}")


# Main execution entry point
if __name__ == "__main__":
    gm = Gate_Manager(GATES_FILE, BACKUP_DIR)
    main_menu(gm)
