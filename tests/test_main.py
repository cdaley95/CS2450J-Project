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

def test_add():
    ml = BasicML()
    ml.accumulator = "+0000"
    ml.accumulator = ml.wrap_around(ml.add_words("+0001", "+0001"))
    assert ml.accumulator == "+0002"
    ml.accumulator = ml.wrap_around(ml.add_words("-0001", "+0001"))
    assert ml.accumulator == "+0000"
    ml.accumulator = ml.wrap_around(ml.add_words("+0002", "+9999"))
    assert ml.accumulator == "-0001"
    
def test_subtract():
    ml = BasicML()
    ml.accumulator = "+0000"
    ml.accumulator = ml.wrap_around(ml.subtract_words("+0001", "+0001"))
    assert ml.accumulator == "+0000"
    ml.accumulator = ml.wrap_around(ml.subtract_words("-0001", "+0002"))
    assert ml.accumulator == "-0003"
    ml.accumulator = ml.wrap_around(ml.subtract_words("+0000", "+0002"))
    assert ml.accumulator == "-0002"

def test_multiply():
    ml = BasicML()
    ml.accumulator = "+0000"
    ml.accumulator = ml.wrap_around(ml.multiply_words("+0001", "+0005"))
    assert ml.accumulator == "+0005"
    ml.accumulator = ml.wrap_around(ml.multiply_words("-0001", "+0005"))
    assert ml.accumulator == "-0005"
    ml.accumulator = ml.wrap_around(ml.multiply_words("+0002", "+5002"))
    assert ml.accumulator == "-0004"

def test_divide():
    ml = BasicML()
    ml.accumulator = "+0000"
    ml.accumulator = ml.wrap_around(ml.divide_words("+0001", "+0001"))
    assert ml.accumulator == "+0001"
    ml.accumulator = ml.wrap_around(ml.divide_words("-0001", "+0001"))
    assert ml.accumulator == "-0001"
