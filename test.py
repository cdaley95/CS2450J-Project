from main import BasicML

# TODO Add testing after core functionality is complete

def test_write():
    test_class = BasicML()

def test_read():
    test_class = BasicML()

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
