import re
Q1 = 0
Q2 = 0

def get_data():
    with open('data.txt') as f:
        mem = ""
        for line in f:
            mem += line.strip()
    return(mem)

def find_and_multiply(string):
    sum = 0
    cmds = re.findall(r'mul\((\d+),(\d+)\)', string)
    for cmd in cmds:
        sum += int(cmd[0]) * int(cmd[1])
    return(sum)

memory = get_data()
Q1 = find_and_multiply(memory)

memory = re.sub(r'don\'t\(\).*?do\(\)', "", memory)
memory = re.sub(r'don\'t\(\).*?$', "", memory)
Q2 = find_and_multiply(memory)

print("Q1: {}".format(Q1))
print("Q2: {}".format(Q2))

