from Blocks import Block,Blocks

def test_get_block_random():
    ptn = {"dot" : [1],

           
           "bar2_h" : [1,1],
           
           "bar2_v" : [[1],
                       [1]],
           
           "bar3_h" : [1,1,1],
           
           "bar3_v" : [[1],
                       [1],
                       [1]],

           "bar4_h" : [1,1,1,1],
           
           "bar4_v" : [[1],
                       [1],
                       [1],
                       [1]],

           "bar5_h" : [1,1,1,1,1],
           
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

    blocks = Blocks()
    b = blocks.get_block_random()
    assert b.name in ptn

def test_block_set():
    blocks = Blocks()
    name = "square_3"
    b = Block(name, blocks.pattern[name])
    assert b.name == name
    assert b.form == [[1,1,1],
                      [1,1,1],
                      [1,1,1]]

def test_pettern_to_block():
    blocks = Blocks()
    for b in blocks.pattern_to_block():
        assert b.name in blocks.pattern.keys()
        assert b.form in blocks.pattern.values()