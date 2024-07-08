'''
Project Name: UVSim
Contributors: Corey Daley, Josh Keyes, Steven Martins, Zachary Wilson
Course: CS2450
Group: J
'''
from tkinter import scrolledtext, filedialog
import tkinter as tk
import os
import time

class BasicML:
    '''Initialized with a 100 word memory and a single
    register named accumulator, as well as a dictionary
    for the opcodes'''
    def __init__(self):
        self.memory = ["+0000"]*100
        self.accumulator = "+0000"
        self.pointer = 0
        self.input = input
        self.print = print

    def exec_instruction(self, instruction_code):
        '''Parses the code into the instruction and the memory location. 
        Also matches the instruction number to the method to execute.'''
        memory_loc = int(instruction_code[3:])
        instruction = instruction_code[1:3]
        match instruction:
            case "10":
                self.read(memory_loc)
            case "11":
                self.write(memory_loc)
            case "20":
                self.load(memory_loc)
            case "21":
                self.store(memory_loc)
            case "30":
                self.add(memory_loc)
            case "31":
                self.subtract(memory_loc)
            case "32":
                self.divide(memory_loc)
            case "33":
                self.multiply(memory_loc)
            case "40":
                self.branch(memory_loc)
            case "41":
                self.branchneg(memory_loc)
            case "42":
                self.branchzero(memory_loc)
            case "43":
                self.halt()
        self.pointer+=1

    def read(self, address):
        'Reads a word from the terminal and stores it in memory'
        usrinput = self.input(f"Word into memory location {address}: ")
        if len(usrinput) == 5:
            if usrinput[0] not in ['+', '-']:
                self.print("Error: 5 character input must be signed 4 digit number.")
                self.halt()
                return
            if not usrinput[1:].isdigit():
                self.print("Error: Input must be signed or unsigned word with digits.")
                self.halt()
                return
        elif len(usrinput) <= 4:
            if usrinput[0] in ['+', '-']:
                if not usrinput[1:].isdigit():
                    self.print("Error: Input must be signed or unsigned word with digits.")
                    self.halt()
                    return
                usrinput = usrinput[0]+usrinput[1:].zfill(4)
            else:
                if not usrinput.isdigit():
                    self.print("Error: Input must be signed or unsigned word with digits.")
                    self.halt()
                    return
                usrinput = "+"+usrinput.zfill(4)
        else:
            self.print("Error: Input cannot have more than 5 characters.")
            self.halt()
            return
        self.memory[address] = usrinput

    def write(self, address):
        'Writes a word from a location in memory to the screen'
        self.print(f"Output: {self.memory[address]}")

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
            self.pointer = address - 1

    def branchneg(self, address):
        'Branches to a specific location in memory if the accumulator is negative'
        if self.accumulator[0] == "-":
            self.pointer = address - 1

    def branchzero(self, address):
        'Branches to a specific location in memory if the accumulator is zero'
        if int(self.accumulator) == 0:
            self.pointer = address - 1

    def halt(self):
        'Stops the program'
        self.pointer = 99
        self.print(" - - Halted Program - - ")

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
            self.print("Error: Cannot divide by zero")
            self.pointer = 100
            return None
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

class MemoryDisplay:
    '''Memory frame class'''
    def __init__(self, root, ml):
        self.root = root
        self.ml = ml

        self.memory_frame = tk.Frame(self.root)
        self.memory_label = tk.Label(self.memory_frame, text="Program Memory")
        self.memory_list = tk.Listbox(self.memory_frame, width=10)
        self.memory_scrollbar = tk.Scrollbar(self.memory_frame, command=self.memory_list.yview)

    def launch(self):
        '''initializes memory frame'''
        self.memory_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.memory_label.pack(side=tk.TOP, pady=5)
        self.memory_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.memory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.memory_list.config(yscrollcommand=self.memory_scrollbar.set)
        for i in range(100):
            self.memory_list.insert(tk.END, f"{i:02}: {self.ml.memory[i]}")

    def update_memory(self):
        '''updates memory in memory display'''
        self.memory_list.delete(0, tk.END)
        for i in range(100):
            self.memory_list.insert(tk.END, f"{i:02}: {self.ml.memory[i]}")

class PointAccumDisplay:
    '''Pointer and Accumulator frame class'''
    def __init__(self, root, ml):
        self.root = root
        self.ml = ml

        self.control_frame = tk.Frame(self.root)

        self.pointer_label = tk.Label(self.control_frame, text="Pointer")
        self.pointer_entry = tk.Entry(self.control_frame, width=3)

        self.accumulator_label = tk.Label(self.control_frame, text="Accumulator")
        self.accumulator_entry = tk.Entry(self.control_frame, width=6)

        self.update_button = tk.Button(self.control_frame,
                    text="Update", command=self.update_both_entry)
        self.reset_button = tk.Button(self.control_frame,
                    text="Reset",
                        command=self.reset_both)

    def launch(self):
        '''initializes control frame'''
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.pointer_label.pack(side=tk.LEFT, padx=5)
        self.pointer_entry.pack(side=tk.LEFT, padx=5)
        self.pointer_entry.insert(0, f"{self.ml.pointer:02}")
        self.pointer_entry.bind("<Return>", self.update_pointer_entry)

        self.accumulator_label.pack(side=tk.LEFT, padx=5)
        self.accumulator_entry.pack(side=tk.LEFT, padx=5)
        self.accumulator_entry.insert(0, f"{self.ml.accumulator}")
        self.accumulator_entry.bind("<Return>", self.update_accumulator_entry)

        self.update_button.pack(side=tk.LEFT, padx=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def reset_pointer(self):
        '''reset pointer to initial value'''
        self.ml.pointer = 0
        self.pointer_entry.delete(0, tk.END)
        self.pointer_entry.insert(0, f"{self.ml.pointer:02}")

    def reset_accumulator(self):
        '''reset accumulator to initial value'''
        self.ml.accumulator = "+0000"
        self.accumulator_entry.delete(0, tk.END)
        self.accumulator_entry.insert(0, f"{self.ml.accumulator}")

    def reset_both(self):
        '''Reset pointer and accumulator to initial values'''
        self.reset_pointer()
        self.reset_accumulator()

    def update_pointer_entry(self, _event=None):
        '''updates the pointer for user modification'''
        try:
            update_pointer = int(self.pointer_entry.get())
            if 0 <= update_pointer < 100:
                self.ml.pointer = update_pointer
                self.pointer_entry.delete(0, tk.END)
                self.pointer_entry.insert(0, f"{self.ml.pointer:02}")
            else:
                self.reset_pointer()
        except ValueError:
            self.reset_pointer()
        self.root.focus_set()

    def update_accumulator_entry(self, _event=None):
        '''updates the accumulator for user modification'''
        try:
            update_accumulator = self.accumulator_entry.get()
            if -9999<= int(update_accumulator) <= 9999:
                if len(update_accumulator) < 5:
                    if update_accumulator[0] in ["-", "+"]:
                        update_accumulator = update_accumulator[0]+update_accumulator[1:].zfill(4)
                    else:
                        update_accumulator = "+"+update_accumulator.zfill(4)
                self.ml.accumulator=update_accumulator
            else:
                self.accumulator_entry.delete(0, tk.END)
                self.accumulator_entry.insert(0, f"{self.ml.accumulator}")
        except ValueError:
            self.accumulator_entry.delete(0, tk.END)
            self.accumulator_entry.insert(0, f"{self.ml.accumulator}")
        self.accumulator_entry.delete(0, tk.END)
        self.accumulator_entry.insert(0, f"{self.ml.accumulator}")
        self.root.focus_set()

    def update_both_entry(self):
        '''update both accumulator and pointer'''
        self.update_accumulator_entry()
        self.update_pointer_entry()

class Controls:
    '''Controls frame class'''
    def __init__(self, root, ml, memory, poiaccu, outin):
        self.root = root
        self.ml = ml
        self.memory = memory
        self.poiaccu = poiaccu
        self.outin = outin
        self.buttons1_frame = tk.Frame(self.root)

        self.load_button = tk.Button(self.buttons1_frame, text="Load File", command=self.load_file)
        self.save_button = tk.Button(self.buttons1_frame, text="Save File", command=self.save_file)

        self.buttons2_frame = tk.Frame(self.root)

        self.run_button = tk.Button(self.buttons2_frame,
                    text="Run Program from Start", command=self.run_fromstart)
        self.continue_button = tk.Button(self.buttons2_frame,
                    text="Continue Program from Pointer", command=self.run_program)
        self.step_button = tk.Button(self.buttons2_frame,
                    text="Step Program", command=self.step_program)

    def launch(self):
        '''initializes button frame'''
        self.buttons1_frame.pack(side = tk.TOP, fill=tk.X)

        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.buttons2_frame.pack(side = tk.TOP, fill=tk.X,)

        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.continue_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.step_button.pack(side=tk.LEFT, padx=5, pady=5)

    def load_file(self):
        '''method for loading file from button click'''
        source_location = filedialog.askopenfilename()
        if source_location == '':
            return
        self.ml.memory = ["+0000"]*100
        self.memory.update_memory()
        self.poiaccu.reset_both()
        if source_location:
            with open(source_location,'r', encoding='utf-8') as file:
                  # Reading lines
                lines = file.readlines()
                # Adding lines to memory
                for line_index, line in enumerate(lines):
                    stripped_line = line.rstrip('\n')
                    if len(stripped_line) != 5:
                        self.outin.gui_output("File contents are not in correct format")
                        self.memory.update_memory()
                        return
                    if stripped_line[0] not in ['+','-']:
                        self.outin.gui_output("File contents are not in correct format")
                        self.memory.update_memory()
                        return
                    if not stripped_line[1:].isdigit():
                        self.outin.gui_output("File contents are not in correct format")
                        self.memory.update_memory()
                        return
                    self.ml.memory[line_index] = stripped_line
                self.memory.update_memory()
                self.poiaccu.reset_both()
        else:
            self.outin.gui_output("File does not exist.")
            return

    def save_file(self):
        '''saves a file from memory location'''
        filename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"), ),
                            defaultextension=".txt")
        if filename == '':
            return
        filename = filename if ".txt" in filename else filename + ".txt"
        with open(filename, 'w', encoding="utf-8") as output:
            for row in self.ml.memory:
                output.write(str(row)+"\n")

    def run_fromstart(self):
        '''runs program from start'''
        self.poiaccu.reset_both()
        self.run_program()

    def run_program(self):
        '''runs program form current pointer location by iterating step program'''
        while int(self.ml.pointer) <= 99:
            self.step_program()

    def step_program(self):
        '''steps the program with one instruction'''
        if self.ml.pointer < 100:
            self.ml.exec_instruction(self.ml.memory[self.ml.pointer])
            self.memory.update_memory()
            self.poiaccu.pointer_entry.delete(0, tk.END)
            self.poiaccu.pointer_entry.insert(0, f"{self.ml.pointer:02}")
            self.poiaccu.accumulator_entry.delete(0, tk.END)
            self.poiaccu.accumulator_entry.insert(0, f"{self.ml.accumulator}")

class ConsoleInputDisplay:
    '''Console and input class'''
    def __init__(self, root, ml):
        self.root = root
        self.ml = ml
        self.ml.print = self.gui_output
        self.ml.input = self.gui_input
        self.console_frame = tk.Frame(self.root)
        self.console_label = tk.Label(self.console_frame, text="Console")
        self.console_text = scrolledtext.ScrolledText(self.console_frame,
                                height=10, state=tk.DISABLED)
        self.console_clearbutton = tk.Button(self.console_frame,
                            text="Clear Console", command=self.clear_console)
        self.input_frame = tk.Frame(self.root)
        self.input_label = tk.Label(self.input_frame, text="Input")
        self.input_entry_var = tk.StringVar()
        self.input_entry = tk.Entry(self.input_frame,
                                     textvariable=self.input_entry_var, state=tk.DISABLED)
        self.input_entry_button = tk.Button(self.input_frame,
                            text="Enter", command=self.handle_enter)
        self.input_received = False

    def launch(self):
        '''initializes input and output frame'''
        self.console_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5)
        self.console_label.pack(side=tk.TOP, pady=5)
        self.console_text.pack(fill=tk.BOTH, expand=True)
        self.console_clearbutton.pack(side=tk.BOTTOM, pady=5)
        self.input_frame.pack(side=tk.TOP, fill=tk.X)
        self.input_label.pack(side=tk.LEFT, padx=5)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        self.input_entry.bind("<Return>", self.handle_enter)
        self.input_entry_button.pack(side=tk.LEFT)

    def gui_output(self, output):
        '''output widget logic'''
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, output + "\n")
        self.console_text.config(state=tk.DISABLED)
        self.console_text.see(tk.END)

    def gui_input(self, prompt):
        '''input entry logic'''
        self.gui_output(prompt)
        self.input_entry.config(state=tk.NORMAL)

        self.input_entry_var.set("")
        self.input_entry.focus_set()

        self.input_received = False

        while not self.input_received:
            self.root.update()
            time.sleep(0.1)

        input_value = self.input_entry_var.get()
        if input_value == "":
            input_value = "+0000"
        elif input_value.isdigit() and len(input_value)<5:
            input_value = "+"+input_value.zfill(4)
        elif input_value[0] == "-" and len(input_value)<6:
            input_value = "-"+input_value[1:].zfill(4)
        else:
            pass
        self.input_entry_var.set("")
        self.input_entry.config(state=tk.DISABLED)

        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, "Input: "+input_value+"\n")
        self.console_text.config(state=tk.DISABLED)
        self.console_text.see(tk.END)

        return input_value

    def clear_console(self):
        '''clears console'''
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.console_text.config(state=tk.DISABLED)

    def handle_enter(self, _event=None):
        '''handles enter key input for user input'''
        self.input_received = True

class BasicMLGUI:
    '''Main GUI class'''
    def __init__(self, ml):
        self.root = tk.Tk()
        self.ml = ml
        self.memory = MemoryDisplay(self.root, self.ml)
        self.poiaccu = PointAccumDisplay(self.root, self.ml)
        self.outin = ConsoleInputDisplay(self.root, self.ml)
        self.controls = Controls(self.root, self.ml, self.memory, self.poiaccu, self.outin)

    def start(self):
        '''sets up GUI window and runs mainloop'''
        self.root.title("UVSim Machine Language Interpreter")
        self.root.iconbitmap(os.path.join(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))), "files","images","icon.ico"))
        self.memory.launch()
        self.poiaccu.launch()
        self.controls.launch()
        self.outin.launch()
        self.root.mainloop()


def main():
    '''main function to run the mainloop'''
    ml_instance = BasicML()
    gui = BasicMLGUI(ml_instance)
    gui.start()

if __name__ == "__main__":
    main()
