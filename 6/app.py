import copy
Q1 = 1
Q2 = 0

def get_data():
    data = []
    with open('sample.txt') as f:
        for line in f:
            data.append(line.strip())
    data = data[::-1]       
    horizontal = []
    vertical = [[] for i in range(0,len(data[0]))]
    start = []
    for y, row in enumerate(data):
        horizontal.append([])
        for x, char in enumerate(row):
            if char == '#':
                horizontal[-1].append(x)
                vertical[x].append(y)
            elif char == "^":
                start = [x,y]
    return(start, horizontal, vertical)

def turn(direction):
    directions = ["N","E","S","W"]
    i = directions.index(direction)
    if i == 3:
        direction = directions[0]
    else:
        direction = directions[i+1]
    return(direction)

def search_path(pos, path, max, inverse=False):
    blocked = False
    #print("   Test Path {}".format(path))
    if not inverse:
        for block in path:
            #print("testing block {}".format(block) )
            if block >= pos:
                new_pos = block - 1
                blocked = True
                break
    else: 
        for block in reversed(path):
            #print("testing inverse block {}: ".format(block))
            if block <= pos:
                new_pos = block + 1
                blocked = True
                break
    if not blocked:
        if not inverse:
            return [-1, max - pos -1, 0]
        else:
            return [-1, pos + 1, 0]
    return(new_pos, abs(new_pos-pos), block)

def check_unique(locations, all_visited):
    i = 0
    for location in locations:
        loc = "{}:{}".format(location[0], location[1])
        if loc not in (all_visited):
            all_visited.append(loc)
        else:
            #print("already been to {}".format(loc))
            next
    return(all_visited)

def move(start, direction, horizontal, vertical, all_visited, test=True):
    test = bool(test)
    max_height = len(horizontal)
    max_width = len(vertical)
    if direction == "N":
        new_pos, steps, next_block = search_path(start[1], vertical[start[0]], max_height, False)
        pos = [start[0], new_pos]
        if new_pos >= 0:
            visited = [[start[0], i] for i in range(start[1], new_pos + 1)]
        else:
            visited = [[start[0], i] for i in range(start[1], max_height)]
    elif direction == "E":
        new_pos, steps, next_block = search_path(start[0], horizontal[start[1]], max_width, False)
        pos = [new_pos, start[1]]
        if new_pos >= 0:
            visited = [[i, start[1]] for i in range(start[0], new_pos + 1)]
        else:
            visited = [[i, start[1]] for i in range(start[0], max_width)]
    elif direction == "S":
        new_pos, steps, next_block = search_path(start[1], vertical[start[0]], max_height, True)
        pos = [start[0], new_pos]
        if new_pos >= 0:
            visited = [[start[0], i] for i in range(new_pos-1, start[1])]
        else:
            visited = [[start[0], i] for i in range(0, start[1])]
    elif direction == "W":
        new_pos, steps, next_block = search_path(start[0], horizontal[start[1]], max_width, True)
        pos = [new_pos, start[1]]
        if new_pos >= 0:
            visited = [[i, start[1]] for i in range(new_pos-1, start[0])]
        else:
            visited = [[i, start[1]] for i in range(0, start[0])]
        
    all_visited = check_unique(visited, all_visited)
    loop_positions = []
    if test:
        
        test_positions = visited
        #print("Will test positions {}".format(visited))
        for test_pos in test_positions:
            i = 0
            test_direction = str(direction)
            test_start = copy.deepcopy(START)
            test_visited = copy.deepcopy(visited)
            test_vertical = copy.deepcopy(vertical)
            test_horizontal = copy.deepcopy(horizontal)

            if test_direction == "N" or test_direction == "S":
                test_vertical[test_pos[0]].append(test_pos[1])
                test_vertical[test_pos[0]].sort()
            if test_direction == "W" or test_direction == "E":
                test_horizontal[test_pos[1]].append(test_pos[0])
                test_horizontal[test_pos[1]].sort()
            looped = False
            test_direction = str(DIRECTION)
            #print("  Testing loop for {} facing {} from {}".format(test_pos, test_direction, test_start))
            loop_test = 0
            loop_coords = []
            while True:
                last_visited = copy.deepcopy(test_visited)

                test_start, test_steps, test_visited, null = move(test_start, test_direction, test_horizontal, test_vertical, test_visited, False)
                
                if len(test_visited) == len(last_visited):
                    loop_test += 1
                    coord_string = "{}:{}:{}".format(test_start[0],test_start[1],test_direction)
                    if coord_string == "96:122:E":
                        print("moved {}".format(steps))
                        print("     Testing loop block at {}".format(test_pos))
                    if len(loop_coords) == 24 and coord_string in loop_coords:
                        looped = True
                        print("  LOOP DETECTED with < 24 repetitions at test pos {} for coords {}".format(test_pos, coord_string))
                        print("    {}".format(loop_coords[-(loop_coords[::-1].index(coord_string)+1):]))
                        break
                    if len(loop_coords) == 24:
                        loop_coords.pop(0)                      
                    loop_coords.append(coord_string)
                    if loop_test == 250:
                        looped = True
                        print("  LONG LOOP DETECTED at {} for {}".format(test_pos, coord_string))
                        break
                elif -1 in test_start:
                    #print("    test case exited map")
                    break
                else:
                    #Not at the end - and have new spaces to test  
                    next
                test_direction = turn(test_direction)
                #print("    TEST: at {} facing {}".format(test_start, test_direction))
                i+= 1
            if looped is True:
                if test_pos[0] not in horizontal[test_pos[1]]:
                    loop_positions.append("{}:{}".format(test_pos[0],test_pos[1]))
                if coord_string == "96:122:E":
                    print(loop_coords)
                    print(coord_string)
                #print(" ---- Block at postion {} loops".format(pos))

    return(pos, steps, all_visited, loop_positions)

start, horizontal, vertical = get_data()
direction = "N"
START = copy.deepcopy(start)
DIRECTION = "N"
done = False
visited = []
loops = []
turns = 0
while not done:
    #print("moving from {} facing {}".format(start, direction))
    start, steps, visited, loop_positions = move(start, direction, horizontal, vertical, visited, True)
    Q1 += steps
    for object in loop_positions:
        if object not in loops:
            loops.append(object)
    #print("  Moved {} steps".format(steps))
    if -1 in start:
        print("EXITED THE MAP")
        done = True
    direction = turn(direction)
    turns += 1

print("Q1 Unique Steps: {}".format(len(visited)))
print(loops)
print("Q2: {}".format(len(loops)))