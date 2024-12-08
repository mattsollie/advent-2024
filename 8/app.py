def get_data():
    with open('data.txt') as f:
        data = {}
        map = []
        
        for y,line in enumerate(f):
            t= []
            height = y
            for x,c in enumerate(line.strip()):
                t.append(c)
                if c != ".":
                    if data.get(c):
                        data[c].append([x,y])
                    else:
                        data[c] = [[x,y]]
                width = x
            map.append(t)
            
    return(data, map, width, height)

def show_map(map, node_coords, nodes=False):
    for node in node_coords:
        map[node[1]][node[0]] = '#'
    for line in map:
        print(''.join(line))

def get_absolute_x(ant, ant_2):
    if ant[0] < ant_2[0]:
        left = ant
        right = ant_2
    else:
        left = ant_2
        right = ant
    return(left, right, right[0] - left[0])

def get_antinodes(ant,ant_2,width, height):
    antinodes = [[],[]]
    left,right, ax = get_absolute_x(ant,ant_2)
    loc = right[0] + ax
    for i in range(right[0],width, ax):
        antinodes[0].append([loc, right[1]])
        loc = loc + ax
    
    loc = left[0] - ax
    for i in range(0, left[0], ax):    
        if loc >= 0:
            antinodes[1].append([loc,left[1]])
            loc = loc - ax
    
    ay = right[1] - left[1]
    if len(antinodes[0]) > 0: #To the right
        for i in range(0,len(antinodes[0])):
            y = antinodes[0][i][1] + (ay * (i+1))
            antinodes[0][i][1] = y

    if len(antinodes[1]) > 0: #To the left
        for i in range(0,len(antinodes[1])):
            y = antinodes[1][i][1] - (ay * (i+1))
            antinodes[1][i][1] = y

    q1_nodes = []
    if len(antinodes[0]) > 0:
        q1_nodes.append(antinodes[0][0])
    if len(antinodes[1]) > 0:
        q1_nodes.append(antinodes[1][0])
    antinodes[0].append(right)                       
    antinodes[1].append(left)      

    return(q1_nodes, antinodes[0] + antinodes[1])


data, map, width, height = get_data()

print("Found antennas: {}".format(data.keys()))
antinodes = []
antinodes2 = []

for frequency in data.keys():
    print("Processing Frequency {}".format(frequency))
    for i, ant in enumerate(data[frequency]):
        print("  Starting Antenna at {}".format(ant))
        for n, ant_2 in enumerate(data[frequency]):
            if n != i:
                print("    2nd Antenna {}".format(ant_2))
                q1_nodes, all_nodes = get_antinodes(ant, ant_2, width, height)
                #Q1
                for antinode in q1_nodes:
                    if antinode not in antinodes and (antinode[0] >=0 and antinode[1] >=0) and (antinode[0] <= width and antinode[1] <= height):
                        antinodes.append(antinode)
                        print("      Antinode: {}".format(antinode))
                #Q2
                for antinode in all_nodes:
                    if antinode not in antinodes2 and (antinode[0] >=0 and antinode[1] >=0) and (antinode[0] <= width and antinode[1] <= height):
                        antinodes2.append(antinode)
                        print("      Antinode_2: {}".format(antinode))
        
print("Q1:")
print(show_map(map, antinodes))
print("Q2:")
print(show_map(map, antinodes2))

print("Q1: {}".format(len(antinodes)))
print("Q2: {}".format(len(antinodes2)))
