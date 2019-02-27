from Logger import Logger
from os import path,remove,linesep
import pytest

@pytest.fixture(scope="function", autouse=True)
def testfile():
    file_name = "D:\\work\\testlog.txt"
    yield file_name
    remove(file_name)

def test_write_log_ini(testfile):
    logger = Logger(log_filepath=testfile)
    logger.write("test")
    assert path.exists(logger.log_filepath)
    with open(logger.log_filepath, mode="r") as rf:
        assert rf.readline().replace("\n","") == "test"


def test_write_log_add(testfile):
    logger = Logger(log_filepath=testfile)
    logger.write("test")
    logger.write("test2")
    with open(logger.log_filepath, mode="r") as rf:
        f_all = rf.read().split("\n\n")
        assert f_all[0] == "test"
        assert f_all[1] == "test2"
