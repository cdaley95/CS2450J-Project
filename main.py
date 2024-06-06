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
        '''
        Loads word from memory address into accumulator
        '''
        self.accumulator = self.memory[int(self.memory[self.pointer][3:])]

    def store(self):
        '''
        Stores word from accumulator into memory address
        '''
        self.memory[int(self.memory[self.pointer][3:])] = self.accumulator

    def read(self):
        '''
        Reads a word from the terminal and stores it in memory
        '''
        word_to_read = input(f"Word to read into memory location {self.memory[self.pointer][3:]}: ")

        # This simply uses the pointer as the spot in memory where this command is being called
        self.memory[int(self.memory[self.pointer][3:])] = word_to_read
    def write(self):
        '''
        Writes a word from a location in memory to the screen
        '''
        print(self.memory[int(self.memory[self.pointer][3:])])

    #Needs a class method to run the program and iterate the pointer


def main():
    '''main method docstring'''
    #need to implement loading from file here
    return

if __name__ == "__main__":
    main()
