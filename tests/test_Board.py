from Board import Board
from Blocks import Block,Blocks
import pytest
import itertools

board_size = 5

@pytest.fixture(scope="function", autouse=True)
def my_board():
    mb = Board(board_size)
    yield mb


def test_board_init(my_board):
    ini = get_plane_board(0)

    assert my_board.now == ini

@pytest.mark.parametrize(
    "x, y", [
        (0,-1),
        (-1,-1),
        (0,-1),
        (board_size,0),
        (0,board_size),
        (board_size,board_size),
        (-1,board_size),
        (board_size,-1)
    ]
)
def test_board_can_set_here_exception_position(my_board,x,y):
    b = Block("test", [[1]])
    assert not my_board.can_set(b,x,y)

@pytest.mark.parametrize(
    "x, y ,b", [
        (board_size-1,0,[[1,1]]),
        (board_size-3,0,[[1,1,1,1]]),
        (0,board_size-1,[[1],[1]]),
        (0,board_size-3,[[1],[1],[1],[1]]),
        (board_size-2,board_size-2,
             [[1],[1],[1],
              [1],[1],[1],
              [1],[1],[1],]),
    ]
)
def test_board_can_set_here_exception_position_2(my_board,x,y,b):
    test_b = Block("test", b)
    assert not my_board.can_set(test_b,x,y)

def test_board_can_set_here_in_empty(my_board):
    blocks = Blocks()
    for n,f in blocks.pattern.items():
        b = Block(n,f)
        assert my_board.can_set(b,0,0)


@pytest.mark.parametrize(
    "x, y ,b, canset", [
        (0,0,[[1]],[]),
        (0,0,[[1,1,1,1]],[]),
        (board_size-3,board_size-1,[[1,1,1]],[]),
        (board_size-1,board_size-3,[[1],[1],[1]],[]),
        (0,0,[[0,1],[1,1]],[(0,0)]),
    ]
    )
def test_board_can_set_here_in_empty2(my_board,x,y,b,canset):
    for i,j in canset:
        my_board.now = set_tst_board_block(my_board.now, i, j, [[1]])
    block = Block("test",b)
    assert my_board.can_set(block,x,y)

def test_board_can_not_set_here(my_board):
    blocks = Blocks()
    
    my_board.now = [[1 for i in range(board_size)] for j in range(board_size)]
    for n,f in blocks.pattern.items():
        b = Block(n,f)
        assert not my_board.can_set(b,0,0)

@pytest.mark.parametrize(
    "cantset_points,block",[
        ([(0,0)],[[1]]),
        ([(0,1),(1,1),(1,0)],[[1,1]]),
       ]
    )
def test_board_can_not_set_here_bacic(my_board,cantset_points,block):
    for i,j in cantset_points:
        my_board.now[i][j] = 1
    b = Block("test",block)
    assert not my_board.can_set(b,0,0)

@pytest.mark.parametrize(
    "x, y ,b", [
        (0,0,[[1]]),
        (0,0,[[1,1,1,1]]),
        (board_size-3,board_size-1,[[1,1,1]]),
        (board_size-1,board_size-3,[[1],[1],[1]])]
    )
def test_set_block_init(my_board,x,y,b):
    test_b = Block("test", b)
    
    after_set_board = \
        set_tst_board_block(
                [[0 for i in range(board_size)] for j in range(board_size)]
            ,   x,y,b)
    
    my_board.set_block(test_b,x,y)

    assert after_set_board == my_board.now

@pytest.mark.parametrize(
    "x, y ,b", [
        (board_size-1,board_size-1,[[1]]),
        (0,board_size-5,[[1 for i in range(board_size-3)]]),
        (board_size-5,board_size-5,[[1 for i in range(board_size-3)]]),
        (2,0,[[1],[1],[1],]),]
    )
def test_set_cant_set(my_board,x,y,b):
    test_b = Block("test", b)
    
    taikakusen = lambda n:[[1 if i==j else 0 for i in range(n)] for j in range(n)] 
    
    now_board = taikakusen(board_size)
    
    setting_block = Block("setting",now_board)
    my_board.set_block(setting_block,0,0) #じゃまブロックセット
    
    my_board.set_block(test_b,x,y)
    
    assert now_board == my_board.now


def test_set_twice(my_board,):
    test_b = Block("test", [[1] for i in range(2)])
    test_b_2 = Block("test2", [[1]])
    
    after_set_board = [[1 if i==3 and j<3 else 0 for i in range(board_size)] for j in range(board_size)]
    
    my_board.set_block(test_b,3,0)
    my_board.set_block(test_b_2,3,2)
    my_board.set_block(test_b_2,3,2)

    assert after_set_board == my_board.now


@pytest.mark.parametrize(
    "x, y, b", [
        (0,0,[[1 for i in range(board_size-1)]]),
        (0,0,[[1] for i in range(board_size-1)]),
        ]
    )
def test_board_update_nodelete(my_board, x, y, b):
    for i,j in  itertools.product(range(x, len(b)) ,range(y, len(b[0]))):
        my_board.now[i][j] = 1

    before = my_board.copy().now
    my_board.update()
    assert before == my_board.now

@pytest.mark.parametrize(
    "x, y, b", [
        (0,0,[[1 for i in range(board_size)]]),
        (0,0,[[1] for i in range(board_size)]),
        (0,0,[[1 for i in range(board_size) if i==0 or j==0] for j in range(board_size)]),
        ]
    )
def test_board_update_delete(my_board, x, y, b):
    for i,j in  itertools.product(range(x, len(b)) ,range(y, len(b[0]))):
        my_board.now[i][j] = 1

    my_board.out_state()
    after = [[0 for i in range(board_size)] for j in range(board_size)]

    my_board.update()
    assert after == my_board.now

def test_board_update_delete_check(my_board):
    b1 = Block("test1", Blocks.pattern["bar2_v"])
    b2 = Block("test2", Blocks.pattern["corner5_ru"])

    after = set_tst_board_block(my_board.now,2,1,b1.form)
    after = set_tst_board_block(after,2,0,b2.form)
    
    my_board.set_block(b1,2,1)
    my_board.set_block(b2,2,0)
    print("\n" + my_board.out_state())
    print("\n", after)
    assert after == my_board.now


def set_tst_board_block(board,x,y,b):
    r = board.copy()
    for x_i in range(0,len(b[0])):
        for y_i in range(0,len(b)):
            r[y+y_i][x+x_i] = r[y+y_i][x+x_i] or b[y_i][x_i]
    return r

def get_plane_board(state=0):
    return [[state for i in range(board_size)] for j in range(board_size)]