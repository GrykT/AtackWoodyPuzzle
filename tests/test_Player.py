from Board import Board
from Blocks import Block,Blocks
from Player import Player
from Pool import Pool
from Brain import Brain, Result_Calc

from collections import deque
import pytest
from unittest.mock import Mock,patch
from os import path
import copy

def make_player(use_block, result_data, board_size):
    mock_pool = Pool(len(result_data),Blocks())
    mock_pool.get_blocks = Mock()
    mock_pool.get_blocks.return_value = use_block

    mock_brain = Brain(Blocks())
    mock_brain.get_setting_info = Mock()
    mock_brain.get_setting_info.side_effect = \
        lambda *a,**k : (copy.deepcopy(deque(result_data)) , 0)
    return Player(mock_pool,Board(board_size),mock_brain,max=10)

@pytest.fixture(scope="function", autouse=True)
def my_player():
    results = []
    b1 = Block("test",[[1]])
    result_1 = Result_Calc(x = 0, y = 0, 
                          block = b1, playable = False)
    results.append(result_1)
    yield(make_player([b1],results,5))

@pytest.fixture(scope="function", autouse=True)
def my_player2():
    results = []
    b2 = Block("test",[[1,1,1,1,1]])
    result_1 = Result_Calc(x = 0, y = 0, 
                          block = b2, playable = True)
    results.append(result_1)
    yield(make_player([b2],results,5))

def test_start_stop(my_player):
    board_size=5
    full_set_board = [[1 for i in range(board_size)] for j in range(board_size)]
    setting_block = Block("setting",full_set_board)
    my_player.set_block(setting_block,0,0)
    result_num = my_player.start()
    assert result_num == 0

def test_stop_max_count(my_player2):
    result_num = my_player2.start()
    assert result_num == my_player2.max_count