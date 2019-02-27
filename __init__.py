from Player import Player
from Board import Board
from Pool import Pool
from Brain import Brain
from Logger import Logger
from Blocks import Blocks
from os import getcwd
from datetime import datetime

#main
if __name__ == "__main__":
    logname = datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")
    player = Player(Pool(3,Blocks())
                    , Board(10),Brain(Blocks())
                    , max=1000
                    , logger=Logger(getcwd() + f"\\log\\woody_log_{logname}.log"))
    result_num = player.start()
    