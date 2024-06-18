'''
Project Name: UVSim
Contributors: Corey Daley, Josh Keyes, Steven Martins, Zachary Wilson
Course: CS2450
Group: J
'''
from tkinter import scrolledtext
import tkinter as tk
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
        '''Parses the code into the instruction and the memory location. 
        Also matches the instruction number to the method to execute.'''
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
                print("Error: 5 character input must be signed.")
                self.pointer=100
                return
            if not usrinput[1:].isdigit():
                print("Error: Input must be signed or unsigned word with digits.")
                self.pointer=100
                return
        elif len(usrinput) <= 4:
            if usrinput[0] in ['+', '-']:
                if not usrinput[1:].isdigit():
                    print("Error: Input must be signed or unsigned word with digits.")
                    self.pointer=100
                    return
                usrinput = "-"+usrinput[1:].zfill(4)
            else:
                if not usrinput.isdigit():
                    print("Error: Input must be signed or unsigned word with digits.")
                    self.pointer=100
                    return
                usrinput = "+"+usrinput.zfill(4)
        else:
            print("Error: Input cannot have more than 5 characters.")
            self.pointer=100
            return
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
        'Converts words to int, sums together, then returns string conversion'
        result = int(word1) + int(word2)
        return f"{result:+05d}"

    def subtract_words(self, word1, word2):
        'Converts words to int, subtracts, then returns string conversion'
        result = int(word1) - int(word2)
        return f"{result:+05d}"

    def divide_words(self, word1, word2):
        'Converts words to int, divides, then returns string conversion'
        if int(word2) == 0:
            print("Error: Cannot divide by zero")
            self.pointer = 100
            return
        result = int(word1) // int(word2)
        return f"{result:+05d}"

    def multiply_words(self, word1, word2):
        'Converts words to int, multiplies, then returns string conversion'
        result = int(word1) * int(word2)
        return f"{result:+05d}"

    def wrap_around(self, word):
        'Converts words to int, multiplies, then returns string conversion'
        if len(word) > 5:
            return word[0]+word[-4:]
        return word

class BasicMLGUI():
    '''GUI for UVSim'''
    def __init__(self, ml, tkin):
        self.root = tkin
        self.ml = ml

        self.root.title("UVSim Machine Language Interpreter")
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        imgdir = os.path.join(parent_dir, "files\\images\\icon.ico")
        self.root.iconbitmap(imgdir)

        self.memory_frame = tk.Frame(self.root)
        self.memory_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.memory_label = tk.Label(self.memory_frame, text="Program Memory")
        self.memory_label.pack(side=tk.TOP, pady=5)
        self.memory_list = tk.Listbox(self.memory_frame, width=10)
        self.memory_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.memory_scrollbar = tk.Scrollbar(self.memory_frame, command=self.memory_list.yview)
        self.memory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.memory_list.config(yscrollcommand=self.memory_scrollbar.set)
        for i in range(100):
            self.memory_list.insert(tk.END, f"{i:02}: {self.ml.memory[i]}")

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.pointer_label = tk.Label(self.control_frame, text="Pointer")
        self.pointer_label.pack(side=tk.LEFT, padx=5)
        self.pointer_entry = tk.Entry(self.control_frame, width=2)
        self.pointer_entry.pack(side=tk.LEFT, padx=5)
        self.pointer_entry.insert(0, f"{self.ml.pointer:02}")

        self.accumulator_label = tk.Label(self.control_frame, text="Accumulator")
        self.accumulator_label.pack(side=tk.LEFT, padx=5)
        self.accumulator_entry = tk.Entry(self.control_frame, width=6)
        self.accumulator_entry.pack(side=tk.LEFT, padx=5)
        self.accumulator_entry.insert(0, f"{self.ml.accumulator:02}")

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(side = tk.TOP, fill=tk.X,)

        self.load_button = tk.Button(self.buttons_frame, text="Load File", command=self.load_file)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.run_button = tk.Button(self.buttons_frame,
                                     text="Run Program", command=self.run_program)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.step_button = tk.Button(self.buttons_frame,
                                      text="Step Program", command=self.step_program)
        self.step_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.console_frame = tk.Frame(self.root)
        self.console_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.console_label = tk.Label(self.console_frame, text="Console")
        self.console_label.pack(side=tk.TOP, pady=5)
        self.console_text = scrolledtext.ScrolledText(self.console_frame,
                                                       height=10, state=tk.DISABLED)
        self.console_text.pack(fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side=tk.TOP, fill=tk.X)
        self.input_label = tk.Label(self.input_frame, text="Input")
        self.input_label.pack(side=tk.LEFT, padx=5)
        self.input_entry_var = tk.StringVar()
        self.input_entry = tk.Entry(self.input_frame, textvariable=self.input_entry_var)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

    def load_file(self):
        pass

    def run_program(self):
        '''while int(self.ml.accumulator) < 100:
            self.step_program()'''

    def step_program(self):
        pass

    def update_pointer(self):
        pass

    def update_accumulator(self):
        pass

    def update_memory(self):
        self.memory_list.delete(0, tk.END)
        for i in range(100):
            self.memory_list.insert(tk.END, f"{i:02}: {self.ml.memory[i]}")


'''def main():
    ''''''main method docstring
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
    print("\nFinished.")'''


if __name__ == "__main__":
    root = tk.Tk()
    mlInstance = BasicML()
    gui = BasicMLGUI(mlInstance, root)
    root.mainloop()
