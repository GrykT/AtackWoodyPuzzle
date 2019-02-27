import random


class Block:
    """block ブロックひとかたまり"""
    def __init__(self,name="", form=[[1]]):
        self.name = name
        self.form = form

class Blocks:
    """blocks ブロックの種類"""
    pattern = {"dot" : [[1]],

           
           "bar2_h" : [[1,1]],
           
           "bar2_v" : [[1],
                       [1]],
           
           "bar3_h" : [[1,1,1]],
           
           "bar3_v" : [[1],
                       [1],
                       [1]],

           "bar4_h" : [[1,1,1,1]],
           
           "bar4_v" : [[1],
                       [1],
                       [1],
                       [1]],

           "bar5_h" : [[1,1,1,1,1]],
           
           "bar5_v" : [[1],
                       [1],
                       [1],
                       [1],
                       [1]],

           "corner3_ru":[[1,1],
                         [0,1]],

           "corner3_rd":[[0,1],
                         [1,1]],

           "corner3_lu":[[1,1],
                         [1,0]],

           "corner3_ld":[[1,0],
                         [1,1]],

           "corner5_ru":[[1,1,1],
                         [0,0,1],
                         [0,0,1]],

           "corner5_rd":[[0,0,1],
                         [0,0,1],
                         [1,1,1]],

           "corner5_lu":[[1,1,1],
                         [1,0,0],
                         [1,0,0]],

           "corner5_ld":[[1,0,0],
                         [1,0,0],
                         [1,1,1]],

           "square_2":[[1,1],
                       [1,1]],

           "square_3":[[1,1,1],
                       [1,1,1],
                       [1,1,1]],
        }
        
    def get_block_random(self):
        name,form = random.choice(list(self.pattern.items()))
        return Block(name,form)

    def pattern_to_block(self):
        return [Block(n,f) for n,f in self.pattern.items()]