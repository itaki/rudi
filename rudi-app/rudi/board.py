import sys
import logging
from . import shop as shop

class BoardManager():

    boards = {}

    def add_board(self, board):
        logging.debug(f"Adding {board['type']}: {board['id']} at {board['connection']}  ")
        self.boards[board["id"]] = BoardFactory(board)

    def add_boards_from_config(self, boards):
        for board in boards:
            self.add_board(board)

    def print_board_list(self):
        print("\n" + "boardS:" + "\n" + "===================================")
        for board_id in self.boards:
            print("    \"" + board_id + "\"")


def BoardFactory(board):

    # would love to make this fully dynamic to not need the classmap
    # inspiration: https://python-course.eu/oop/dynamically-creating-classes-with-type.php

    # or can we at least move into the board_library?

    classmap = {
        'ServoHat': ServoHat
    }
    return classmap[board["type"]](board)








    # import of specific device classes must happen after parent "Device" class is defined above
sys.path.append('../rudi')
from rudi.board_library import *