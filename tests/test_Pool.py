from Pool import Pool
from Blocks import Blocks

import pytest

@pytest.fixture(scope="function", autouse=True)
def my_pool():
    pool_size = 3
    blocks = Blocks()
    yield Pool(pool_size, blocks)

def test_init(my_pool):
    pool_size = 3
    assert len(my_pool.get_blocks()) == pool_size

def test_get_full_blocks(my_pool):
    blocks = Blocks()
    assert all([b.name in blocks.pattern.keys() for b in my_pool.get_blocks()])

#poolからpopして取る仕様はやめ
#def test_get_block_twice(my_pool):
#    full = my_pool.get_blocks()
#    used = my_pool.get_blocks()
#    assert all([u.name in [f.name for f in full] for u in used])
#
#def test_pop_block(my_pool):
#    get = my_pool.get_blocks()
#    b = my_pool.pop_block(0)
#    re_get = my_pool.get_blocks()
#    assert len(re_get) == 2
#
#def test_pop_block_loop(my_pool):
#    get = my_pool.get_blocks()
#    for i in range(3):
#        b = my_pool.pop_block(0)
#    assert len(my_pool.stock) == 0
#
#    re_get = my_pool.get_blocks()
#    assert len(re_get) == 3

