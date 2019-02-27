from Player import Player
from Board import Board
from Pool import Pool
from Brain import Brain
from Logger import Logger
from Blocks import Blocks
from os import getcwd
from datetime import datetime
from sys import argv

#main
if __name__ == "__main__":
    board_size = int(argv[1] if len(argv) > 1 else 5)
    logname = datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")
    player = Player(Pool(3,Blocks())
                    , Board(board_size),Brain(Blocks())
                    , max=1000
                    , logger=Logger(getcwd() + f"\\log\\woody_log_{logname}.log"))
    result_num = player.start()
    