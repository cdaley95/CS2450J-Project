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
                self.pointer+=1
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
    basic_ml = BasicML()
    # TODO Allow for file input
    source_location = input("Name and location of file: ")
    # source_location = "test.txt"

    # Reading and adding lines to memory
    try:
        with open(source_location, 'r') as file:
            # Reading lines
            lines = file.readlines()
            # Adding lines to memory
            for line_index in range(0, len(lines)):
                basic_ml.memory[line_index] = lines[line_index][:5]
    except:
        print("Not a valid file location.")
        return
    # Executing lines from memory
    while basic_ml.pointer != 100:
        basic_ml.exec_instruction(basic_ml.memory[int(basic_ml.pointer)])
    print("\nFinished.")


if __name__ == "__main__":
    main()
