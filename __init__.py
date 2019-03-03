from Player import Player
from Board import Board
from Pool import Pool
from Brain import Brain
from Logger import Logger
from Blocks import Blocks
from os import getcwd
from datetime import datetime
from sys import argv
from itertools import product
from functools import reduce
from math import gcd

#main
if __name__ == "__main__":
    board_size = int(argv[1] if len(argv) > 1 else 5)
    learn_swith = argv[2] if len(argv) > 2 else ""
    logname = datetime.strftime(datetime.now(),"%Y%m%d%H%M%S")

    player = Player(Pool(3,Blocks())
                    , Board(board_size)
                    , Brain(Blocks(),weights=(100, 1, 10, 1))
                    , max=1000
                    , logger=Logger(getcwd() + f"\\log\\woody_log_{logname}.log"))
    
    if(learn_swith == "-l"):
        w1 = (1,10,100)
        w2 = (1,10,100)
        w3 = (1,10,100)
        w4 = (1,10,100)
        already = []
        for a1,a2,a3,a4 in product(w1,w2,w3,w4):
            its_gcd = reduce(gcd,[a1,a2,a3,a4])
            regl = (a1/its_gcd, a2/its_gcd, a3/its_gcd, a4/its_gcd)
            if regl in already:
                #重み付けの比が一緒ならやる必要なし
                print(f"{(a1,a2,a3,a4)}は{regl}なのでskip")
                continue
            else:
                already.append(regl)
                player.add_brain(Brain(Blocks(),weights=(a1,a2,a3,a4)))
        
        result_set = player.start_learn()
        print([(num, br.weights) for num,br in result_set])

    else:
        result_num = player.start()


    