'''
Project Name: UVSim
Contributors: Corey Daley, Josh Keyes, Steven Martins, Zachary Wilson
Course: CS2450
Group: J
'''


class BasicML:
    '''Initialized with a 100 word memory and a single
    register named accumulator, as well as a dictionary
    for the opcodes'''

    def __init__(self):
        self.memory = ["+0000"]*100
        self.accumulator = "+0000"
        self.pointer = 0

        # Dictionary mapping opcodes to class methods
        self.instructions = {
            10: self.read,
            11: self.write,
            20: self.load,
            21: self.store,
            30: self.add,
            31: self.subtract,
            32: self.divide,
            33: self.multiply,
            40: self.branch,
            41: self.branchneg,
            42: self.branchzero,
            43: self.halt
        }

    def read(self, address):
        'Reads a word from the terminal and stores it in memory'
        self.memory[address] = input(f"Word into memory location {address}: ")

    def write(self, address):
        'Writes a word from a location in memory to the screen'
        print(self.memory[address])

    def load(self, address):
        'Loads word from memory address into accumulator'
        self.accumulator = self.memory[address]

    def store(self, address):
        'Stores word from accumulator into memory address'
        self.memory[address] = self.accumulator

    def branch(self, address):
        'Branches to a specific location in memory'
        self.pointer = address

    def branchneg(self, address):
        'Branches to a specific location in memory if the accumulator is negative'
        if self.accumulator[0] == "-":
            self.pointer = address

    def branchzero(self, address):
        'Branches to a specific location in memory if the accumulator is zero'
        if self.accumulator == "+0000":
            self.pointer = address

    def halt(self):
        'Stops the program'
        self.pointer = 100

    def load(self):
        'Loads word from memory address into accumulator'
        address = int(self.memory[self.pointer][3:])
        self.accumulator = self.memory[address]
        self.pointer += 1

    def store(self):
        'Stores word from accumulator into memory address'
        address = int(self.memory[self.pointer][3:])
        self.memory[address] = self.accumulator
        self.pointer += 1

    def add(self):
        'Adds word from memory address to accumulator'
        address = int(self.memory[self.pointer][3:])
        self.accumulator = self.wrap_around(self.add_words(self.accumulator, self.memory[address]))
        self.pointer += 1

    def subtract(self):
        'Subtracts word from memory address from accumulator'
        address = int(self.memory[self.pointer][3:])
        self.accumulator = self.wrap_around(self.subtract_words(self.accumulator, self.memory[address]))
        self.pointer += 1

    def divide(self):
        'Divides accumulator by word from memory address'
        address = int(self.memory[self.pointer][3:])
        self.accumulator = self.wrap_around(self.divide_words(self.accumulator, self.memory[address]))
        self.pointer += 1

    def multiply(self):
        'Multiplies accumulator by word from memory address'
        address = int(self.memory[self.pointer][3:])
        self.accumulator = self.wrap_around(self.multiply_words(self.accumulator, self.memory[address]))
        self.pointer += 1

    def add_words(self, word1, word2):
        result = int(word1) + int(word2)
        return f"{result:+05d}"

    def subtract_words(self, word1, word2):
        result = int(word1) - int(word2)
        return f"{result:+05d}"

    def divide_words(self, word1, word2):
        if int(word2) == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = int(word1) // int(word2)
        return f"{result:+05d}"

    def multiply_words(self, word1, word2):
        result = int(word1) * int(word2)
        return f"{result:+05d}"

    def wrap_around(self, word):
        num = int(word)
        limit = 9999
        while num > limit or num < -limit:
            if num > limit:
                num = -(num - limit - 1)
            elif num < -limit:
                num = -(num + limit + 1)
        return f"{num:+05d}"
    # Needs a class method to run the program and iterate the pointer


def main():
    '''main method docstring'''
    # Need to implement loading from file here
    return


if __name__ == "__main__":
    main()
