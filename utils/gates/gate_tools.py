import curses
import sys
import time
import os
import questionary as q

from adafruit_servokit import ServoKit

from styles import custom_style_dope, get_styles


# Create single-ended input on channel 0
kit = ServoKit(channels=16, address=0x42)

keyboard_present = True



def gate_setter(gate,direction):
    """checking for keypress"""
    key = 0
    adjustment = 0
    angle = 90 #set the servo in the middle
    # Create new standard Screen
    stdscr = curses.initscr()
    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed

    while (key != ord('q')):

        # Initialization
        stdscr.clear()

        height, width = stdscr.getmaxyx()



        # Declaration of strings
        title = "Set Gates"[:width-1]
        subtitle = "Use arrow keys"[:width-1]
        keystr = "Last key pressed: {}".format(key)[:width-1]
        statusbarstr = f"Press 'q' to exit | STATUS BAR | Pos: {angle}"
        if key == 0:
            keystr = "Use arrow keys to adjust. 0 to recenter. return to accept. q to quit"[:width-1]

        if key != 0:
            keystr = "I've been hit"
        if key == curses.KEY_DOWN:
            keystr = "I've been hit DOWN"
            adjustment = -1
        if key == curses.KEY_LEFT:
            adjustment = -10
        if key == curses.KEY_UP:
            adjustment = 1
        if key == curses.KEY_RIGHT:
            adjustment = 10
        if key == ord('0'):
            angle = 89
            adjustment = 1
        if adjustment != 0:
            angle = angle + adjustment
            adjustment = 0 
            if angle > 180:
                statusbarstr = "WARNING - MAX angle is 180!!!"
                angle = 180
            if angle < 0: 
                statusbarstr = "WARNING - MIN angle is 0!!!"
                angle = 0
            

            kit.servo[0].angle = angle

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)




        # Wait for next input
        key = stdscr.getkey()
        stdscr.addstr(5,5, f"key: {key}")

        # Refresh the screen
        stdscr.refresh()
        stdscr.getch()


class Gate_Manager:
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


if __name__ == "__main__":
    gm = Gate_Manager(GATES_FILE)
    main_menu(gm)
