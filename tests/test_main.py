import pytest

from src.main import BasicML


@pytest.mark.parametrize("address, expected", [
    (0, "+1234"),
    (1, "+2345"),
    (2, "+3456"),
    (3, "+4567"),
    (4, "+5678")
])
def test_write(address, expected, capsys):
    ml = BasicML()
    ml.memory = ["+1234", "+2345", "+3456", "+4567", "+5678"]
    ml.write(address)
    captured = capsys.readouterr()
    assert captured.out == expected + "\n"


@pytest.mark.parametrize("address, expected", [
    (0, "+1234"),
    (1, "+2345"),
    (2, "+3456"),
    (3, "+4567"),
    (4, "+5678")
])
def test_load(address, expected):
    ml = BasicML()
    ml.memory = ["+1234", "+2345", "+3456", "+4567", "+5678"]
    ml.load(address)
    assert ml.accumulator == expected


@pytest.mark.parametrize("address, expected", [
    (0, "+1234"),
    (1, "+2345"),
    (2, "+3456"),
    (3, "+4567"),
    (4, "+5678")
])
def test_store(address, expected):
    ml = BasicML()
    ml.accumulator = expected
    ml.store(address)
    assert ml.memory[address] == expected


@pytest.mark.parametrize("address", [
    (5),
    (4),
    (3),
    (2),
    (1)
])
def test_branch(address):
    ml = BasicML()
    ml.branch(address)
    assert ml.pointer == address


@pytest.mark.parametrize("address", [
    (5),
    (4),
    (3),
    (2),
    (1)
])
def test_branchneg(address):
    ml = BasicML()
    ml.accumulator = "-1234"
    ml.branchneg(address)
    assert ml.pointer == address


@pytest.mark.parametrize("address", [
    (5),
    (4),
    (3),
    (2),
    (1)
])
def test_branchzero(address):
    ml = BasicML()
    ml.accumulator = "+0000"
    ml.branchzero(address)
    assert ml.pointer == address


def test_halt():
    ml = BasicML()
    ml.halt()
    assert ml.pointer == 100

def test_load_1():
    loadtest1 = BasicML()
    loadtest1.memory[0:3] = ["+2002","+1054","-9756"]
    loadtest1.load()
    assert loadtest1.accumulator == "-9756"

def test_load_2():
    loadtest2 = BasicML()
    loadtest2.memory[66:69] = ["-2068","+1010","+8888"]
    loadtest2.pointer = 66
    loadtest2.load()
    assert loadtest2.accumulator == "+8888"

def test_store_1():
    storetest1 = BasicML()
    storetest1.memory[0:2] = ["-2102","+1030"]
    storetest1.accumulator = "-9645"
    storetest1.store()
    assert storetest1.memory[2] == "-9645"

def test_store_2():
    storetest2 = BasicML()
    storetest2.memory[89:92] = ["+2169","+1030","-5674"]
    storetest2.accumulator = "-7532"
    storetest2.pointer = 89
    storetest2.store()
    assert storetest2.memory[69] == "-7532"
