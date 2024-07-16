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
from theme import theme


class BasicML:
    '''Initialized with a 250 word memory and a single
    register named accumulator'''
    def __init__(self):
        self.memory = ["+000000"]*250
        self.accumulator = "+000000"
        self.pointer = 0
        self.input = input
        self.print = print
        self.update_callback = None

    def set_update_callback(self, callback):
        '''sets callback function'''
        self.update_callback = callback

    def notify_update(self):
        '''callback if set'''
        if self.update_callback:
            self.update_callback()

    def loaddata(self, addr, data):
        '''loads data into memory'''
        self.memory[addr] = data
        self.notify_update()

    def exec_instruction(self, instruction_code):
        '''Parses the code into the instruction and the memory location. 
        Also matches the instruction number to the method to execute.'''
        memory_loc = int(instruction_code[4:])
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
        self.pointer += 1
        self.notify_update()

    def read(self, address):
        'Reads a word from the terminal and stores it in memory'
        usrinput = self.input(f"Word into memory location {address}: ")
        if len(usrinput) == 7:
            if usrinput[0] not in ['+', '-']:
                self.print("Error: 7 character input must be signed 6 digit number.")
                self.halt()
                return
            if not usrinput[1:].isdigit():
                self.print("Error: Input must be signed or unsigned word with digits.")
                self.halt()
                return
        elif len(usrinput) < 7:
            if usrinput[0] in ['+', '-']:
                if not usrinput[1:].isdigit():
                    self.print("Error: Input must be signed or unsigned word with digits.")
                    self.halt()
                    return
                usrinput = usrinput[0]+usrinput[1:].zfill(6)
            else:
                if not usrinput.isdigit():
                    self.print("Error: Input must be signed or unsigned word with digits.")
                    self.halt()
                    return
                usrinput = "+"+usrinput.zfill(6)
        else:
            self.print("Error: Input cannot have more than 7 characters.")
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
        self.pointer = 249
        self.print(" - - Halted Program - - ")

    def add_words(self, word1, word2):
        'Converts words to int, sums together, then returns string conversion'
        result = int(word1) + int(word2)
        return f"{result:+07d}"

    def subtract_words(self, word1, word2):
        'Converts words to int, subtracts, then returns string conversion'
        result = int(word1) - int(word2)
        return f"{result:+07d}"

    def divide_words(self, word1, word2):
        'Converts words to int, divides, then returns string conversion'
        if int(word2) == 0:
            self.print("Error: Cannot divide by zero")
            self.pointer = 250
            return None
        result = int(word1) // int(word2)
        return f"{result:+07d}"

    def multiply_words(self, word1, word2):
        'Converts words to int, multiplies, then returns string conversion'
        result = int(word1) * int(word2)
        return f"{result:+07d}"

    def wrap_around(self, word):
        'Converts words to int, multiplies, then returns string conversion'
        if len(word) > 7:
            return word[0]+word[-6:]
        return word

    def run_program(self):
        '''runs program'''
        while self.pointer < 250:
            self.exec_instruction(self.memory[self.pointer])

class BasicMLExec:
    '''layer for executing BasicML program'''
    def __init__(self, ml, poiaccu):
        self.ml = ml
        self.poiaccu = poiaccu

    def step_program(self):
        '''steps program'''
        if self.ml.pointer < 250:
            self.ml.exec_instruction(self.ml.memory[self.ml.pointer])

    def run_program(self):
        '''runs program form current pointer'''
        self.ml.run_program()

    def run_fromstart(self):
        '''runs program from start'''
        self.cleardata(0, 1, 1)
        self.ml.run_program()

    def cleardata(self, mem, poi, acc):
        '''clears data'''
        if mem:
            mem = ["+000000"]*250
        if acc:
            acc = "+000000"
        if poi:
            poi = "0"
        self.updatedata(mem, poi, acc)

    def updatedata(self, mem, poi, acc):
        '''updates data'''
        if mem:
            self.ml.memory = mem
        if poi:
            self.ml.pointer = int(poi)
        if acc:
            self.ml.accumulator = acc
        self.ml.notify_update()


class FileManager:
    '''manages loading and saving files'''
    def __init__(self, ml, execu):
        self.ml = ml
        self.exec = execu

    def load_file(self):
        '''load file contents to memory'''
        filename = filedialog.askopenfilename()
        if filename == '':
            return
        self.exec.cleardata(1, 1, 1)
        if filename:
            with open(filename,'r', encoding='utf-8') as file:
                  # Reading lines
                lines = file.readlines()
                # Adding lines to memory
                for line_index, line in enumerate(lines):
                    stripped_line = line.rstrip('\n')
                    if len(stripped_line) != 5:
                        return "error2"
                    if stripped_line[0] not in ['+','-']:
                        return "error2"
                    if not stripped_line[1:].isdigit():
                        return "error2"
                    self.ml.loaddata(line_index,
                                     ''.join((stripped_line[0:3]+"00"+stripped_line[3:])))
                self.exec.cleardata(None, 1, 1)
        else:
            return "error1"

    def save_file(self):
        '''save file to directory'''
        filename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"), ),
                            defaultextension=".txt")
        if filename == '':
            return
        filename = filename if ".txt" in filename else filename + ".txt"
        with open(filename, 'w', encoding="utf-8") as output:
            for row in self.ml.memory:
                output.write(str(row)+"\n")

class MemoryDisplay:
    '''Memory frame class'''

    def __init__(self, mainwindow):
        '''Initializes memory frame'''
        self.mainwindow = mainwindow
        self.root = self.mainwindow.root
        self.ml = self.mainwindow.ml

        self.memory_frame = tk.Frame(self.root, background=theme["background"])
        self.memory_label = tk.Label(self.memory_frame, background=theme["background"],
                                     text="Program Memory", fg=theme["text"])
        self.save_memory_button = tk.Button(self.memory_frame,
                                            text="Save Memory", background=theme["foreground"],
                                            activebackground=theme["active_foreground"],
                                            command=self.save, fg=theme["text"])
        self.line_numbers = tk.Text(self.memory_frame,
                                    width=5,
                                    state="disabled", background=theme["text_background"])
        self.memory_text = tk.Text(self.memory_frame,
                                   width=14, background=theme["text_background"])
        self.memory_scrollbar = tk.Scrollbar(self.memory_frame,
                                             command=self.memory_text.yview,
                                             background=theme["scroll_bar"],
                                             troughcolor=theme["scroll_bar_background"],
                                             activebackground=theme["active_foreground"])

    def launch(self):
        '''Finishes initializing memory frame'''
        self.memory_frame.pack(side=tk.LEFT,
                               fill=tk.BOTH,
                               expand=True,
                               padx=5)
        self.memory_label.pack(side=tk.TOP,
                               pady=5)
        self.save_memory_button.pack(side=tk.BOTTOM,
                                     pady=5)
        self.line_numbers.pack(side=tk.LEFT,
                               fill=tk.Y)
        self.memory_text.pack(side=tk.LEFT,
                              fill=tk.BOTH,
                              expand=True)
        self.memory_scrollbar.pack(side=tk.RIGHT,
                                   fill=tk.Y)

        # Ties both text widgets to the scrollbar
        self.line_numbers.config(yscrollcommand=self.memory_scrollbar.set)
        self.memory_text.config(yscrollcommand=self.memory_scrollbar.set)

        # Checks for new lines on each keypress and updates line numbers
        self.memory_text.bind("<KeyRelease>", self.update_line_numbers)

        self.load()
        self.sync_scroll()

    def load(self):
        '''Loads memory into memory frame'''
        self.memory_text.delete("1.0", tk.END)

        for i in range(250):
            if i < 249:
                self.memory_text.insert(tk.END, f"{self.ml.memory[i]}\n")
            else:
                self.memory_text.insert(tk.END, f"{self.ml.memory[i]}")

        self.update_line_numbers()

    def save(self):
        '''Saves memory from memory frame'''
        content = self.memory_text.get("1.0", "end-1c")
        lines = content.splitlines()

        if len(lines) > 250:
            return self.ml.print("Error: Memory cannot exceed 250 entries.")

        for index, line in enumerate(lines):
            if len(line) != 7:
                return self.ml.print(f"Error: Word in register #{index:03} "
                                     "must be 7 characters.")
            elif line[0] not in ["+", "-"]:
                return self.ml.print(f"Error: Word in register #{index:03} "
                                     "must be signed.")
            elif not line[1:].isdigit():
                return self.ml.print(f"Error: Word in register #{index:03} "
                                     "must be a number.")

        for index, line in enumerate(lines):
            self.ml.memory[index] = line

        # Fill remaining memory with 0s preventing issues when loading
        # a small program after having loaded a larger one
        for i in range(len(lines), 250):
            self.ml.memory[i] = "+000000"
        self.mainwindow.update_display()

        self.ml.print("Memory saved successfully.")

    def scroll_position(self):
        '''Gets scroll position'''
        return self.memory_scrollbar.get()[0]

    def update_line_numbers(self, _event=None):
        '''Updates line numbers'''
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)

        line_count = int(self.memory_text.index('end-1c').split('.', maxsplit=1)[0])
        content = "\n".join(f"{i:03}:" for i in range(line_count))

        self.line_numbers.insert("1.0", content)
        self.line_numbers.config(state="disabled")

        self.line_numbers.yview_moveto(self.scroll_position())

    def sync_scroll(self):
        '''Syncs scroll'''
        self.line_numbers.yview_moveto(self.scroll_position())
        self.memory_text.yview_moveto(self.scroll_position())

        # Calls itself every 25ms
        self.memory_scrollbar.after(25, self.sync_scroll)

class PointAccumDisplay:
    '''Pointer and Accumulator frame class'''
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.root = self.mainwindow.root
        self.ml = self.mainwindow.ml
        self.exec = BasicMLExec(self.mainwindow.ml, self)

        self.control_frame = tk.Frame(self.root, background=theme["background"])

        self.pointer_label = tk.Label(self.control_frame, fg=theme["text"],
                                      text="Pointer",
                                      background=theme["background"])
        self.pointer_entry = tk.Entry(self.control_frame, width=4,
                                      background=theme["text_background"])
        self.update_pointer_button = tk.Button(self.control_frame, fg=theme["text"],
                                               text="Update Pointer",
                                                command=self.update_pointer_entry,
                                                background=theme["foreground"],
                                                activebackground=theme["active_foreground"])

        self.accumulator_label = tk.Label(self.control_frame, fg=theme["text"],
                                          text="Accumulator", background=theme["background"])
        self.accumulator_entry = tk.Entry(self.control_frame, width=8,
                                          background=theme["text_background"])
        self.update_accumulator_button = tk.Button(self.control_frame,
                    fg=theme["text"], text="Update Accumulator",
                    command=self.update_accumulator_entry,
                    background=theme["foreground"], activebackground=theme["active_foreground"])
        self.reset_button = tk.Button(self.control_frame,
                    fg=theme["text"], text="Reset",
                        command=self.reset_both, background=theme["foreground"],
                        activebackground=theme["active_foreground"])

    def launch(self):
        '''initializes control frame'''
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.pointer_label.pack(side=tk.LEFT, padx=5)
        self.pointer_entry.pack(side=tk.LEFT, padx=5)
        self.pointer_entry.insert(0, f"{self.ml.pointer:03}")
        self.pointer_entry.bind("<Return>", self.update_pointer_entry)
        self.update_pointer_button.pack(side=tk.LEFT, padx=5)

        self.accumulator_label.pack(side=tk.LEFT, padx=5)
        self.accumulator_entry.pack(side=tk.LEFT, padx=5)
        self.accumulator_entry.insert(0, f"{self.ml.accumulator}")
        self.accumulator_entry.bind("<Return>", self.update_accumulator_entry)
        self.update_accumulator_button.pack(side=tk.LEFT, padx=5)

        self.reset_button.pack(side=tk.LEFT, padx=5)

    def reset_pointer(self):
        '''reset pointer to initial value'''
        self.exec.cleardata(0, 1, 0)

    def reset_accumulator(self):
        '''reset accumulator to initial value'''
        self.exec.cleardata(0, 0, 1)

    def reset_both(self):
        '''Reset pointer and accumulator to initial values'''
        self.exec.cleardata(0, 1, 1)

    def update_pointer_entry(self, _event=None):
        '''updates the pointer for user modification'''
        try:
            update_pointer = int(self.pointer_entry.get())
            if 0 <= update_pointer < 250:
                self.exec.updatedata(None, str(update_pointer), None)
            else:
                self.reset_pointer()
        except ValueError:
            self.reset_pointer()
        self.root.focus_set()

    def update_accumulator_entry(self, _event=None):
        '''updates the accumulator for user modification'''
        try:
            update_accumulator = self.accumulator_entry.get()
            if -999999 <= int(update_accumulator) <= 999999:
                if len(update_accumulator) < 7:
                    if update_accumulator[0] in ["-", "+"]:
                        update_accumulator = update_accumulator[0]+update_accumulator[1:].zfill(6)
                    else:
                        update_accumulator = "+"+update_accumulator.zfill(6)
                self.exec.updatedata(None, None, update_accumulator)
            else:
                self.reset_accumulator()
        except ValueError:
            self.reset_accumulator()
        self.root.focus_set()

class Controls:
    '''Controls frame class'''
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.root = self.mainwindow.root
        self.ml = self.mainwindow.ml
        self.memory = self.mainwindow.memory
        self.poiaccu = self.mainwindow.poiaccu
        self.outin = self.mainwindow.outin
        self.exec = BasicMLExec(self.ml, self.poiaccu)
        self.fileman = FileManager(self.ml, self.exec)
        self.buttons1_frame = tk.Frame(self.root, background=theme["background"])

        self.load_button = tk.Button(self.buttons1_frame, fg=theme["text"], text="Load File",
                                     command=self.load_file, background=theme["foreground"],
                                     activebackground=theme["active_foreground"])
        self.save_button = tk.Button(self.buttons1_frame, fg=theme["text"], text="Save File",
                                     command=self.save_file, background=theme["foreground"],
                                     activebackground=theme["active_foreground"])

        self.buttons2_frame = tk.Frame(self.root, background=theme["background"])

        self.run_button = tk.Button(self.buttons2_frame,
                    fg=theme["text"], text="Run Program from Start", command=self.run_fromstart,
                    background=theme["foreground"], activebackground=theme["active_foreground"])
        self.continue_button = tk.Button(self.buttons2_frame,
                    fg=theme["text"], text="Continue Program from Pointer",
                    command=self.run_program, background=theme["foreground"],
                    activebackground=theme["active_foreground"])
        self.step_button = tk.Button(self.buttons2_frame,
                    fg=theme["text"], text="Step Program", command=self.step_program,
                    background=theme["foreground"], activebackground=theme["active_foreground"])

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
        info = self.fileman.load_file()
        if info == "error1":
            self.outin.gui_output("File does not exist.")
            return
        if info == "error2":
            self.outin.gui_output("File contents are not in correct format")
            return
        return

    def save_file(self):
        '''saves a file from memory location'''
        self.fileman.save_file()

    def run_fromstart(self):
        '''runs program from start'''
        self.exec.run_fromstart()

    def run_program(self):
        '''runs program form current pointer'''
        self.exec.run_program()

    def step_program(self):
        '''steps the program with one instruction'''
        self.exec.step_program()

class ConsoleInputDisplay:
    '''Console and input class'''
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.root = self.mainwindow.root
        self.console_frame = tk.Frame(self.root, background=theme["background"])
        self.console_label = tk.Label(self.console_frame, fg=theme["text"],
                                       text="Console", background=theme["background"])
        self.console_text = scrolledtext.ScrolledText(self.console_frame,
                                height=10, state=tk.DISABLED)
        ##
        self.console_text.configure(background=theme["text_background"])
        self.console_text.vbar.configure(background=theme["scroll_bar"],
                                          troughcolor=theme["scroll_bar_background"],
                                          activebackground=theme["active_foreground"])

        ##
        self.console_clearbutton = tk.Button(self.console_frame,
                            fg=theme["text"], text="Clear Console", command=self.clear_console,
                            background=theme["foreground"],
                            activebackground=theme["active_foreground"])
        self.input_frame = tk.Frame(self.root, background=theme["background"])
        self.input_label = tk.Label(self.input_frame, fg=theme["text"],
                                    text="Input", background=theme["background"])
        self.input_entry_var = tk.StringVar()
        self.input_entry = tk.Entry(self.input_frame,
                                     textvariable=self.input_entry_var,
                                     state=tk.DISABLED,background=theme["text_background"],
                                     disabledbackground=theme["text_background"])
        self.input_entry_button = tk.Button(self.input_frame,
                            fg=theme["text"], text="Enter",
                            command=self.handle_enter, background=theme["foreground"],
                            activebackground=theme["active_foreground"])
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
        self.input_entry.config(state=tk.NORMAL, background=theme["text_background"],
                                foreground=theme["text_background"])

        self.input_entry_var.set("")
        self.input_entry.focus_set()

        self.input_received = False

        while not self.input_received:
            self.root.update()
            time.sleep(0.1)

        input_value = self.input_entry_var.get()
        if input_value == "":
            input_value = "+000000"
        elif input_value.isdigit() and len(input_value) < 7:
            input_value = "+"+input_value.zfill(6)
        elif input_value[0] == "-" and len(input_value) < 8:
            input_value = "-"+input_value[1:].zfill(6)
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
    def __init__(self):
        self.root = tk.Tk()
        self.ml = BasicML()
        self.memory = MemoryDisplay(self)
        self.poiaccu = PointAccumDisplay(self)
        self.outin = ConsoleInputDisplay(self)
        self.controls = Controls(self)
        self.ml.print = self.outin.gui_output
        self.ml.input = self.outin.gui_input
        self.ml.set_update_callback(self.update_display)

    def update_display(self):
        '''updates the display whenever there's a change in BasicML'''
        self.memory.load()
        self.poiaccu.pointer_entry.delete(0, tk.END)
        self.poiaccu.pointer_entry.insert(0, f"{self.ml.pointer:03}")
        self.poiaccu.accumulator_entry.delete(0, tk.END)
        self.poiaccu.accumulator_entry.insert(0, f"{self.ml.accumulator}")

    def start(self):
        '''sets up GUI window and runs mainloop'''
        self.root.title("UVSim Machine Language Interpreter")
        self.root.configure(background=theme["background"])
        self.root.iconbitmap(os.path.join(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))), "files","images","icon.ico"))
        self.memory.launch()
        self.poiaccu.launch()
        self.controls.launch()
        self.outin.launch()
        self.root.mainloop()

if __name__ == "__main__":
    gui = BasicMLGUI()
    gui.start()
