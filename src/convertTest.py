def process_file(input_file):
    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.strip()
            if len(line) == 5:
                new_line = line[:1] + '0' + line[1:3] + '0' + line[3:]
                print(new_line)

file = "src\Test2.txt"
process_file(file)


