from copy import deepcopy
Q1 = 0
Q2 = 0

def get_data():
    with open('/home/matt/repos/advent-2024/9/data.txt') as f:
        data = []
        for line in f:
            data.append(line.strip())
    return(data)

def print_disk(map, ret_str=True): #Used for Q2 to build flat array
    array = []
    for i,n in enumerate(map["free"]):
        for a in map["blocks"][i]:
            if len(a) > 0:
                for c in a:
                    array.append(str(c))
        for p in range(0,n):
            array.append(".")
        if ret_str is True:
            ret = ''.join(array)
        else:
            ret = array
    return(ret)

map = {"blocks":[],"free":[]}
disk_map = get_data()[0]
modes = ['blocks','free']
i = 0
id = 0

for char in disk_map:
    mode = modes[i]
    if mode == "blocks":
        data = [id for i in range(0,int(char))]
        id += 1
    else:
        data = int(char)
    map[mode].append(data)
    i = 0 if i == 1 else 1

map2 = deepcopy(map) 
# Q1
iter = 0
for i,m in enumerate(map["free"]):
    num_blocks = m
    moved_blocks = 0
    iter += 1
    while moved_blocks < num_blocks:
        print("Processing Space {} itteration {}".format(i,iter))
        remaining_blocks = num_blocks - moved_blocks
        if len(map["blocks"][-1]) <= remaining_blocks:
            # Move whole sequence
            moving_blocks = map["blocks"].pop(-1)
            map["blocks"].insert(iter,moving_blocks)
            moved_blocks += len(moving_blocks)
        else:
            # Move partial sequence
            block_len = len(map["blocks"][-1])
            moving_blocks = map["blocks"][-1][block_len - remaining_blocks:]
            map["blocks"][-1] = map["blocks"][-1][:block_len - remaining_blocks]
            map["blocks"].insert(iter,moving_blocks)
            moved_blocks += len(moving_blocks)
        iter += 1

#Q2
# Put all blocks into an array so we can track where spaces go later
for i,block in enumerate(map2["blocks"]):
    map2["blocks"][i]=[block]

for i,f in enumerate(map2["blocks"][::-1]):
    file = f[0]
    for n,m in (enumerate(map2["free"][0:len(map2["blocks"]) - 1 - i])):
        if len(file) <= m:
            file_pos = len(map2["blocks"]) - 1 - i #Since file's are itterating backwards
            map2["blocks"][file_pos].pop(0) #remove the first file - It's the original
            map2["blocks"][n].append(file)  #append to earlier sequence
            map2["free"][file_pos-1] += len(file) # Add free space where we're getting this number from
            map2["free"][n] -= len(file) # Subract free space where we're moving it to
            break

disk_blocks = []
for a in map["blocks"]: #Flatten the blocks to single array, ignore free space
    disk_blocks += a
for i,id in enumerate(disk_blocks):
    Q1 += i * id

for i,id in enumerate(print_disk(map2,False)):
    if id != ".": #This is a string array 
        Q2 += int(id) * i
 
print("Q1: {}".format(Q1))
print("Q2: {}".format(Q2))