from copy import deepcopy
Q1, Q2 = 0, 0

def get_data():
    with open('/home/matt/repos/advent-2024/10/data.txt') as f:
        data = []
        trailheads = []
        for y, line in enumerate(f):
            data.append([])
            for x,char in enumerate(line.strip()):
                data[-1].append(int(char))
                if int(char) == 0:
                    trailheads.append((x,y))                    
    return(data, trailheads)

def get_coord(map,coord,dir=None):
    x, y = coord[0], coord[1]
    if dir == "N":
        y -= 1
    elif dir == "S":
        y += 1
    elif dir == "W":
        x -= 1
    elif dir == "E":
        x += 1
    return([map[y][x], (x,y)])

def get_neighbors(map, pos, elevation = None):
    width = len(map[0])-1
    height = len(map)-1
    possible_moves =[]
    a = []
    if pos[1] > 0:
        a.append(get_coord(map, pos, "N"))
    if pos[1] < height:
        a.append(get_coord(map, pos, "S"))
    if pos[0] > 0:
        a.append(get_coord(map, pos, "W"))
    if pos[0] < width:
        a.append(get_coord(map, pos, "E"))
    if elevation is not None:
        for c in a:
            if c[0] == elevation + 1:
                possible_moves.append(c[1])
    else:
                possible_moves = [c for c in a]
    return(possible_moves)


def find_path_end(map,pos,elevation):
    paths = [{"elevation": elevation, "path": [pos]}]
    done = False
    while not done:
        done = True
        for i,path in enumerate(paths):
            if path["path"][-1] != "X" and get_coord(map, path["path"][-1])[0] != 9:
                print("Processing Loop from {} {} at elevation{}".format(path["path"][-1], i, path["elevation"]))
                done = False
                moves = get_neighbors(map,path["path"][-1],path["elevation"])
                if len(moves) == 0:
                    paths[i]["path"].append("X")
                    print("stopping at elevation {}".format(path["elevation"]))
                    next
                if len(moves) >= 1:
                    print("One Move: {} at elevation {}".format(moves[0], paths[i]["elevation"]))
                    paths[i]["elevation"] += 1
                    paths[i]["path"].append(moves[0])
                if len(moves) > 1:
                    for m in moves[1:]:
                        print("Alternate Move: {} at elevation {}".format(moves[0], paths[i]["elevation"]))
                        paths.append(deepcopy(path))
                        paths[-1]["path"].pop(-1)
                        paths[-1]["path"].append(m)
            else:
                print("Path Complete {} at elevation{}".format(i, path["elevation"]))

    final_path = []
    final_values = []
    q2_paths = 0
    for i,path in enumerate(paths):
        if "X" not in path["path"]:
            q2_paths +=1
            for coord in path["path"]:
                if coord not in final_path:
                    final_path.append(coord)
                    final_values.append(get_coord(map,coord)[0])

    return(final_path, final_values, q2_paths)


map, trailheads = get_data()
scores = []

for trailhead in trailheads:
    elevation, coord = get_coord(map, trailhead)
    coords, elevations, rating = find_path_end(map,coord,elevation)
    score = elevations.count(9)
    scores.append(score)
    Q2 += rating

print("Q1: {}".format(sum(scores)))
print("Q2: {}".format(Q2))