from Brain import Brain
from Blocks import Block,Blocks
from Board import Board
import pytest
from collections import deque
import itertools

board_size = 3

@pytest.fixture(scope="function", autouse=True)
def my_board():
    bd = Board(board_size)
    yield bd

@pytest.fixture(scope="function", autouse=True)
def tst_block():
    bl = [Block(("test",[[1]]))]
    yield bl

@pytest.fixture(scope="function", autouse=True)
def my_brain():
    br = Brain(Blocks())
    yield br

def test_get_setting_info_init(my_brain,my_board,tst_block):
    res,eval = my_brain.get_setting_info(my_board, tst_block)
    assert 0 <= res[0].x < board_size
    assert 0 <= res[0].y < board_size
    assert res[0].block.form == tst_block[0].form
    assert res[0].playable

def test_calc_cant_set(my_brain, my_board, tst_block):
    my_board.now[0][0] = 1
    results,eval = my_brain.get_setting_info(my_board, tst_block)

    for r in results:
        assert (r.x,r.y) != (0,0)

def test_search_settable_point(my_brain,my_board,tst_block):
    pts = my_brain.search_settable_point(my_board, tst_block[0])
    assert len(pts) == board_size ** 2


@pytest.mark.parametrize(
    "cantset_points", [
        [],
        [(0,0)],
        [(x,0) for x in range(board_size)],
     ]
    )
def test_search_settable_point2(my_brain,my_board,tst_block,cantset_points):
    for i,j in cantset_points:
        my_board.now[i][j] = 1

    pts = my_brain.search_settable_point(my_board, tst_block[0])
    for p in pts:
        assert p not in cantset_points


@pytest.mark.parametrize(
    "cantset_points", [
        [(x,y) for x in range(board_size) for y in range(board_size)],
     ]
    )
def test_search_settable_point_cantset(my_brain,my_board,tst_block,cantset_points):
    for i,j in cantset_points:
        my_board.now[i][j] = 1

    pts = my_brain.search_settable_point(my_board, tst_block[0])
    assert len(pts) == 0


@pytest.mark.parametrize(
    "cantset_points", [
        [],
        [(0,0)],
        [(x,0) for x in range(board_size)],
     ]
    )
def test_search_blocks_of_a_permutation_setting(my_brain,my_board,tst_block,cantset_points):
    for i,j in cantset_points:
        my_board.now[i][j] = 1

    tst_block.append(Block(("test2",[[1,1]])))
    tst_block.append(Block(("test3",[[1],[1]])))

    results,eval = my_brain.search_blocks_of_a_permutation_setting(my_board,tst_block,[0,1,2])

    for i in range(len(results)):
        assert results[i].playable
        assert 0 <= results[i].x < board_size
        assert 0 <= results[i].y < board_size
        assert results[i].block.name == tst_block[i].name

@pytest.mark.parametrize(
    "cantset_points", [
        [[1 if x!=y else 0 for x in range(board_size)] for y in range(board_size)],
     ]
    )
def test_search_blocks_of_a_permutation_setting_cant(my_brain,my_board,cantset_points):
    my_board.now = cantset_points

    tst_blk=[]
    tst_blk.append(Block("test1",[[1,1]]))
    tst_blk.append(Block("test2",[[1,1]]))
    tst_blk.append(Block("test3",[[1],[1]]))

    results,eval = my_brain.search_blocks_of_a_permutation_setting(my_board,tst_blk,[0,1,2])
    
    for i in range(len(results)):
        assert not results[i].playable
        assert results[i].block.name == tst_blk[i].name


@pytest.mark.parametrize(
    "tst_b", [
        ([
            Block("t1",[[1]]),
            Block("t2",[[1,1,1]]),
            Block("t3",[[1],[1],[1]])
         ])
     ]
    )
def test_search_blocks_of_a_permutation_setting_secondblock_cantplay(my_brain,my_board,tst_b):
    my_board.now = [[0 if x!=y else 1 for x in range(board_size)] for y in range(board_size)]
    
    result,eval = my_brain.search_blocks_of_a_permutation_setting(my_board,tst_b,[0,1,2])
    
    r_1 = result.popleft()
    assert r_1.playable
    r_2 = result.popleft()
    assert not r_2.playable


def test_search_all_permutation_blocks(my_brain,my_board,tst_block):
    tst_block.append(Block(("test2",[[1 for i in range(board_size)]])))
    tst_block.append(Block(("test3",[[1] for i in range(board_size)])))

    result,eval = my_brain.search_all_permutation_blocks(my_board,tst_block)

    assert_res = []
    block_num = len(tst_block)
    for p in itertools.permutations(range(block_num),block_num):
        res,eval = my_brain.search_blocks_of_a_permutation_setting(my_board,tst_block,list(p))
        assert_res.append([res,eval])

    zipped = list(zip(*assert_res))
    evals = list(zipped[1])
    assert_res_max = max(assert_res, key=lambda r : r[1] == max(evals))[0]
    
    assert eval == max(evals)
    for i in range(len(result)):
        assert result[i].playable
        assert result[i].block.name in [ast.block.name for ast in assert_res_max]


@pytest.mark.parametrize(
    "tst_b", [
        ([
            Block("t1",[[1,1]]),
            Block("t2",[[1],[1]]),
            Block("t3",[[1,1],[1]])
         ])
     ]
    )
def test_search_all_permutation_blocks_cantplay(my_brain,my_board,tst_b):
    my_board.now = [[1 if x!=y else 0 for x in range(board_size)] for y in range(board_size)]
    result,eval = my_brain.search_all_permutation_blocks(my_board,tst_b)
    
    for r in result:
        assert not r.playable


def test_count_space_ini(my_brain,my_board):
    assert my_board.size ** 2 == my_brain.count_space((my_board.size ** 2), my_board.now)

def test_count_space(my_brain,my_board):
    my_board.now[0][0] = 1
    my_board.now[0][1] = 1
    assert (my_board.size ** 2) - 2 == my_brain.count_space((my_board.size ** 2), my_board.now)


@pytest.mark.parametrize(
    "mask,expect", [
        ([[0 for x in range(board_size)] for y in range(board_size)], 1),
        ([[1 for x in range(board_size)] for y in range(board_size)], 0),
     ]
    )
def test_count_settable_kinds_of_block(my_brain,my_board,tst_block,mask,expect):
    my_board.now = mask
    kinds = my_brain.count_settable_kinds_of_block(my_board,tst_block)
    assert kinds == expect

@pytest.mark.parametrize(
    "mask,expect", [
        ([[0 for x in range(board_size)] for y in range(board_size)], 0),
        ([[1 for x in range(board_size)] for y in range(board_size)], 12+20*(board_size-2)+8*(board_size-2)**2),
     ]
    )
def test_count_around_block(my_brain,my_board,tst_block,mask,expect):
    my_board.now = mask
    sum_around = my_brain.count_around_block(my_board)
    assert sum_around == expect

