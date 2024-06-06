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

    # Needs a class method to run the program and iterate the pointer


def main():
    '''main method docstring'''
    # Need to implement loading from file here
    return


if __name__ == "__main__":
    main()
