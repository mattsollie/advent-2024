import re
from math import floor, prod
import statistics

def move_robots(seconds, robots, size):
    max_x, max_y = size[0], size[1]    
    for r in robots:
        for sec in range(seconds):
            x,y = r[0][0] + r[1][0] , r[0][1] + r[1][1]
            if x >= max_x:
                x = x - max_x
            elif x < 0:
                x = max_x + x
            if y >= max_y:
                y = y - max_y
            elif y < 0:
                y = max_y + y
            r[0] = (x,y)
    return(robots)

def get_v(robots):
    x_a = [x[0][0] for x in robots]
    y_a = [x[0][1] for x in robots]
    x_v = statistics.variance(x_a)
    y_v = statistics.variance(y_a)
    return [x_v, y_v]

def get_score(robots, size):
    max_x, max_y  = size[0] - 1, size[1] - 1
    mid_x, mid_y = floor((size[0]/2) -1), floor((size[1] /2) -1)
    quads = [[(0,0), (mid_x , mid_y)],[(mid_x+2, 0), (max_x,mid_y)],[(0,mid_y+2), (mid_x, max_y)],[(mid_x+2, mid_y+2),(max_x,max_y)]]
    score = [0,0,0,0]
    
    for r in robots:
        pos = r[0]
        for i,q in enumerate(quads):
                if pos[0] >= q[0][0] and pos[0] <= q[1][0] and pos[1] >= q[0][1] and pos[1] <= q[1][1]:
                    score[i] += 1
    return(score)
    
def get_data():
    with open('/home/matt/repos/advent-2024/14/sample.txt') as f:
        data = []
        for line in f:
            m = re.search(r'=(.+)\,(.+)\sv=(.+)\,(.+)',line.strip())
            data.append([(int(m[1]),int(m[2])),(int(m[3]),int(m[4]))])
    return(data)

def get_map(map, data):
    map_a = []
    for y in range(map[1]):
        map_a.append(["." for x in range(map[0])])

    for r in data:
        if map_a[r[0][1]][r[0][0]] == ".":
            map_a[r[0][1]][r[0][0]]  = 1
        else:
            map_a[r[0][1]][r[0][0]]  += 1

    for l in map_a:
        for i, c in enumerate(l):
            if isinstance(c, int):
                l[i] = str(c)
        print(''.join(l))

map_size = (101,103)
#Q1
data = get_data()
data = move_robots(100, data, map_size)
score = get_score(data, map_size)
get_map(map_size, data)

#Q2
data = get_data()
sec = 0
v = get_v(data)
x_variance = [v[0]]
y_variance = [v[1]]
tree = False
check_tree = False
while not tree:
    sec += 1
    data = move_robots(1, data, map_size)
    v = get_v(data)
    v_x = statistics.mean(x_variance)
    v_y = statistics.mean(y_variance)
    if (v[1] > (v_y * 1.5) or v[1] < (v_y * .47)) and  (v[0] > (v_x * 1.64) or v[0] < (v_x * .33)): #Yes, I tuned this after finding it looking at dozens of these
        check_tree = True
    
    if check_tree:
        get_map(map_size, data)
        check_tree = False
        tree = True
    else: #Only add the normal ones to keep the average narrow
        x_variance.append(v[0])
        y_variance.append(v[1])

print("Q1: {}".format(prod(score)))
print("Q2: {}".format(sec))

