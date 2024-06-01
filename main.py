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

        #Dictionary mapping opcodes to class methods
        self.instructions = {
            20: self.load,
            21: self.store
        }

    def load(self):
        'Loads word from memory address into accumulator'
        self.accumulator = self.memory[int(self.memory[self.pointer][3:])]

    def store(self):
        'Stores word from accumulator into memory address'
        self.memory[int(self.memory[self.pointer][3:])] = self.accumulator

    #Needs a class method to run the program and iterate the pointer


def main():
    '''main method docstring'''
    #need to implement loading from file here
    return

if __name__ == "__main__":
    main()
