import numpy as np
import itertools
import copy

class Board:
    """Board 盤面　状態保持、消える判定して消す、画面出力"""
    def __init__(self,size):
        self.size = size
        self.now = [[0 for i in range(size)] for j in range(size)]

    def can_set(self,block,x,y):
        """
        blockを基点(x,y)に置けるか判定
        """
        if x < 0 or self.size - 1 < x:
            return False

        if y < 0 or self.size - 1 < y:
            return False

        len_h = block.h
        len_w = block.w

        if x + len_w > self.size:
            return False

        if y + len_h > self.size:
            return False

        set_range = [w[x:x+len_w] for w in self.now[y:y+len_h]]
        
        and_calc = np.array(block.form) * np.array(set_range)
        zero_range = np.zeros((len_w,len_h), dtype=object)

        return (and_calc == zero_range).all()


    def set_block(self,block,x,y):
        """
        ボードにブロックを置く
        """
        if(self.can_set(block,x,y)):
            for x_i in range(0,len(block.form[0])):
                for y_i in range(0,len(block.form)):
                    self.now[y+y_i][x+x_i] = self.now[y+y_i][x+x_i] or block.form[y_i][x_i]

            self.update()
        #else:
        #    print("そこ置けない")

    def update(self):
        """
        縦横そろってたら消す。同時に揃った場合も消すこと
        """
        horizontal = [idx for idx, i in enumerate(self.now) if all([r==1 for r in self.now[idx]])]

        now_T = np.array(self.now).T #インデックス取りやすくするために転置
        vertical = [idx for idx, i in enumerate(now_T) if all([r==1 for r in now_T[idx]])]

        for i in horizontal:
            self.now[i] = [0 for j in range(self.size)]

        for i,j in itertools.product(range(self.size),vertical):
            self.now[i][j] = 0

    def out_state(self):
        trans_dic = {0:"□" ,1:"■"}
        flat = ""
        for line in self.now:
            for pnt in line:
                #print(trans_dic[pnt], end="")
                flat += trans_dic[pnt]
            #print("", end="\n")
            flat += "\n"
        return flat

    def copy(self):
        copy_board = Board(self.size)
        copy_board.now = copy.deepcopy(self.now)
        return copy_board