'''
Project Name: UVSim
Contributors: Corey Daley, Josh Keyes, Steven Martins, Zachary Wilson
Course: CS2450
Group: J
'''
import os

class BasicML:
    '''Initialized with a 100 word memory and a single
    register named accumulator, as well as a dictionary
    for the opcodes'''

    def __init__(self):
        self.memory = ["+0000"]*100
        self.accumulator = "+0000"
        self.pointer = 0

    def exec_instruction(self, instruction_code):
        '''Parses the code into the instruction and the memory location. Also matches the instruction number to the method to execute.'''
        memory_loc = int(instruction_code[3:])
        instruction = instruction_code[1:3]
        match instruction:
            case "10":
                self.read(memory_loc)
                self.pointer += 1
            case "11":
                self.write(memory_loc)
                self.pointer += 1
            case "20":
                self.load(memory_loc)
                self.pointer += 1
            case "21":
                self.store(memory_loc)
                self.pointer += 1
            case "30":
                self.add(memory_loc)
                self.pointer += 1
            case "31":
                self.subtract(memory_loc)
                self.pointer += 1
            case "32":
                self.divide(memory_loc)
                self.pointer += 1
            case "33":
                self.multiply(memory_loc)
                self.pointer += 1
            case "40":
                self.branch(memory_loc)
            case "41":
                self.branchneg(memory_loc)
            case "42":
                self.branchzero(memory_loc)
            case "43":
                self.halt()

    def read(self, address):
        'Reads a word from the terminal and stores it in memory'
        usrinput = input(f"Word into memory location {address}: ")
        if len(usrinput) == 5:
            if usrinput[0] not in ['+', '-']:
                raise ValueError("Input must either signed 5 character or unsigned 4 character word with 4 digits.")
            if not usrinput[1:].isdigit():
                raise ValueError("Input must either signed 5 character or unsigned 4 character word with 4 digits.")
        elif len(usrinput) == 4:
            if not usrinput.isdigit():
                raise ValueError("Input must either signed 5 character or unsigned 4 character word with 4 digits.")
            else:
                usrinput = "+"+usrinput
        else:
             raise ValueError("Input must either signed 5 character or unsigned 4 character word with 4 digits.")
        self.memory[address] = usrinput

    def write(self, address):
        'Writes a word from a location in memory to the screen'
        print(self.memory[address])

    def load(self, address):
        'Loads word from memory address into accumulator'
        self.accumulator = self.memory[address]

    def store(self, address):
        'Stores word from accumulator into memory address'
        self.memory[address] = self.accumulator

    def add(self, address):
        'Adds word from memory address to accumulator'
        self.accumulator = self.wrap_around(
            self.add_words(self.accumulator, self.memory[address]))

    def subtract(self, address):
        'Subtracts word from memory address from accumulator'
        self.accumulator = self.wrap_around(
            self.subtract_words(self.accumulator, self.memory[address]))

    def divide(self, address):
        'Divides accumulator by word from memory address'
        self.accumulator = self.wrap_around(
            self.divide_words(self.accumulator, self.memory[address]))

    def multiply(self, address):
        'Multiplies accumulator by word from memory address'
        self.accumulator = self.wrap_around(
            self.multiply_words(self.accumulator, self.memory[address]))

    def branch(self, address):
        'Branches to a specific location in memory if accumulator is positive'
        if self.accumulator[0] == "+":
            self.pointer = address
        else:
            self.pointer += 1

    def branchneg(self, address):
        'Branches to a specific location in memory if the accumulator is negative'
        if self.accumulator[0] == "-":
            self.pointer = address
        else:
            self.pointer += 1

    def branchzero(self, address):
        'Branches to a specific location in memory if the accumulator is zero'
        if int(self.accumulator) == 0:
            self.pointer = address
        else:
            self.pointer += 1

    def halt(self):
        'Stops the program'
        self.pointer = 100

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
        if len(word) > 5:
            return word[0]+word[2:]
        return word


def main():
    '''main method docstring'''
    basic_ml = BasicML()
    # TODO Allow for file input
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_location = os.path.join(parent_dir, "files", input("Name of file: "))
    print(source_location)
    # source_location = "test.txt"

    # Reading and adding lines to memory
    try:
        with open(source_location, 'r') as file:
            # Reading lines
            lines = file.readlines()
            # Adding lines to memory
            for line_index, line in enumerate(lines):
                stripped_line = line.rstrip('\n')
                if len(stripped_line) != 5:
                    raise ValueError("File contents are not in correct format")
                if stripped_line[0] not in ['+','-']:
                    raise ValueError("File contents are not in correct format")
                if not stripped_line[1:].isdigit():
                    raise ValueError("File contents are not in correct format")
                basic_ml.memory[line_index] = stripped_line
    except FileNotFoundError:
        print("Not a valid file location.")
        return
    except ValueError as e:
        print(e)
        return
    # Executing lines from memory
    while basic_ml.pointer != 100:
        basic_ml.exec_instruction(basic_ml.memory[int(basic_ml.pointer)])
    print("\nFinished.")


if __name__ == "__main__":
    main()
