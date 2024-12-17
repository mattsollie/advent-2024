from math import floor, ceil, modf

class Room:
    def __init__ (self, map, boxes, robot, max_x, max_y, grid, version):
        self.pos_x = robot[0]
        self.pos_y = robot[1]
        self.map = map
        self.boxes = boxes
        self.max_x = max_x
        self.max_y = max_y
        self.grid = grid
        self.version = version

    def display(self, zoom=False):
        state = []
        for i,l in enumerate(self.grid):
            state.append(l.copy())
            for b in self.boxes[i]:
                state[-1][b] = 'O'
            if self.pos_y == i:
                state[-1][self.pos_x] = "@"
        if zoom:
            for l in state[self.pos_y-4:self.pos_y+4]:
                print(''.join(l[self.pos_x-4:self.pos_x+4]))
        else:
            for l in state:
                print(''.join(l))

    def display2(self, zoom=False):
        state = []
        for i,l in enumerate(self.grid):
            state.append(l.copy())
            for b in self.boxes[i]:
                state[-1][int(b*2)] = '['
                state[-1][int((b*2)+1)] = ']'
            if self.pos_y == i:
                state[-1][int(self.pos_x * 2)] = "@"
        if zoom:
            for l in state[self.pos_y-4:self.pos_y+4]:
                print(''.join(l[self.pos_x-4:self.pos_x+4]))
        else:
            for l in state:
                print(''.join(l))

    def score(self):
        score = 0
        for n, r in enumerate(self.boxes):
            for b in r:
                if self.version == 1:
                    score += (100 * n) + b
                else:
                    score += (100 * n) + (b*2)
        return(score)

    def check_offset(self, check, y, robot = False):
        pos_x = check[0]
        pos_y = check[1]

        
        if robot:
            boxes = [i for i, x in enumerate(self.boxes) if pos_x in x or pos_x -.5 in x]
            walls = [i for i, x in enumerate(self.map) if pos_x in x or pos_x -.5 in x]
        else:
            boxes = [i for i, x in enumerate(self.boxes) if pos_x in x or pos_x -.5 in x or pos_x +.5 in x]
            walls = [i for i, x in enumerate(self.map) if pos_x in x or pos_x -.5 in x or pos_x +.5 in x ]
        print(boxes)
        print(walls)
        blocked = False
        moving = []
        if (pos_y + y) in walls: # wall - skip
            print("   Hit Wall")
            blocked = True
        elif (pos_y + y) not in  walls and (pos_y + y) in boxes: #no wall, but a box
            print("    Blocked box location")
            if pos_x in self.boxes[pos_y + y]:
                moving.append((pos_x, pos_y + y))
            if pos_x + .5 in self.boxes[pos_y + y] and not robot:
                moving.append((pos_x + .5, pos_y + y))
            if pos_x - .5 in self.boxes[pos_y + y]:
                moving.append((pos_x - .5, pos_y + y))
        return(blocked, moving)

    def move(self, char):
        print("Move {}".format(char))
        x,y = 0,0
        if char == '<':
            x -= 1
        elif char == '>':
            x += 1
        elif char == 'v':
            y += 1
        elif char == '^':
            y-= 1
        if self.version == 2:
            x = x/2
        
        if x != 0:
            print("  Move {} to {}".format(self.pos_x, self.pos_x + x))
            if (self.pos_x + x) in self.map[self.pos_y]: # wall - skip
                print("    Hit Wall")
            elif (self.pos_x + x -.5 ) in self.map[self.pos_y] and x < 0: # wall - skip?
                print("    Hit Wall")
            elif float(floor(self.pos_x + x)) not in self.map[self.pos_y] and float(floor(self.pos_x + x)) not in self.boxes[self.pos_y] and (self.pos_x + x) not in self.map[self.pos_y] and (self.pos_x + 2*x) not in self.boxes[self.pos_y] and x<0: #Open position
                #Push Left
                print("    Open location")
                self.pos_x = self.pos_x + x
            elif float(floor(self.pos_x + x)) not in self.map[self.pos_y] and float(floor(self.pos_x + x)) not in self.boxes[self.pos_y] and (self.pos_x + x) not in self.map[self.pos_y] and (self.pos_x + x) not in self.boxes[self.pos_y] and x>0: #Open position
                #Push Right
                print("    Open location")
                self.pos_x = self.pos_x + x
            elif float(floor(self.pos_x + x)) not in self.map[self.pos_y] and ((self.pos_x + x) in self.boxes[self.pos_y] or (self.pos_x + (2*x)) in self.boxes[self.pos_y]): #no wall, but a box
                print(" Box Location Row {}".format(self.boxes[self.pos_y]))
                found = False
                s = self.pos_x + x
                while found == False and s > 0 and s < max_x:
                    if floor(s) in self.map[self.pos_y]:
                        break
                    elif floor(s) not in self.map[self.pos_y] and (floor(s) not in self.boxes[self.pos_y] and s not in self.boxes[self.pos_y] and (s + .5)) and x>0:
                        found = True
                        print(s)
                    elif floor(s) not in self.map[self.pos_y] and (s not in self.boxes[self.pos_y] and s not in self.boxes[self.pos_y] and (s - .5) not in self.boxes[self.pos_y]) and x<0:
                        found = True
                        print(s)
                    else:
                        s += 2*x
                        print("testing x {}".format(2*x))
                if found:
                    positions = []
                    print("    blocked spaces from {} to {}. Next Open space {}".format(self.pos_x + x, s, s))
                    if x>0:
                        if modf(x)[0] == 0.5:
                            positions = list(range(int(self.pos_x + x), int(ceil(s))))
                        else:    
                            positions = list(range(int(floor(self.pos_x + x)), int(s +1)))
                        d = []
                        for p in positions:
                            d.append(float(p))
                            d.append(p + .5)
                        positions = d
                    else:
                        if modf(x)[0] == 0.5:
                            positions = list(range(int(floor(s)), int(floor(self.pos_x))))
                        else:
                            positions = list(range(int(floor(s)), int(floor(self.pos_x))))
                            positions.append(self.pos_x - .5)
                        d = []
                        for p in positions:
                            d.append(float(p))
                            d.append(p + .5)
                        positions = d
                    positions.sort(reverse=x>0)
                    print("will check positions {}".format(positions))
                    for i in positions:
                        if i in self.boxes[self.pos_y]:
                            print("move {} by {}".format(self.boxes[self.pos_y][self.boxes[self.pos_y].index(i)], x))
                            self.boxes[self.pos_y][self.boxes[self.pos_y].index(i)] += x
                    print(" Row {}".format(self.boxes[self.pos_y]))
                    self.pos_x = self.pos_x + x
                else:
                    print("no free space found")
            else:
                print("Somehow slipped through")        
                print(float(floor(self.pos_x + x)) not in self.map[self.pos_y])
                print((float(floor(self.pos_x + x)) in self.boxes[self.pos_y]))
                print((self.pos_x + x) in self.boxes[self.pos_y])
        else:
            print("  Move {} to {}".format(self.pos_y, self.pos_y + y))
            boxes = [i for i, x in enumerate(self.boxes) if self.pos_x in x or self.pos_x -.5 in x]
            walls = [i for i, x in enumerate(self.map) if self.pos_x in x or self.pos_x -.5 in x]
            
            if (self.pos_y + y) not in  walls and (self.pos_y + y) not in boxes and (self.pos_y + y -.5) not in walls and (self.pos_y + y - .5) not in boxes: #Open position
                print("   Open location")
                self.pos_y = self.pos_y + y
            else:
                blocked = False
                moving = []
                check = [(self.pos_x, self.pos_y)]
                robot = True
                while blocked is False:
                    l_block = False
                    l_m = []
                    for c in check:
                        blocked, m = self.check_offset(c,y, robot)
                        if blocked:
                            l_block = True
                        else:
                            l_m += m
                    if l_block:
                        blocked = True
                    if len(l_m) == 0:
                        break
                    else:
                        moving += l_m
                        check = l_m
                    robot=False

                
                if blocked: # wall - skip
                    print("   Hit Wall")
                elif len(moving) > 0: #no wall, but a box
                    print("    Blocked location but movable {}".format(moving))
                    moving = list(set(moving))
                    for b in moving:
                        print("move {} by {}".format(b, y))
                        self.boxes[b[1]+y].append(self.boxes[b[1]].pop(self.boxes[b[1]].index(b[0])))
                    self.pos_y = self.pos_y + y    

def get_data(version=1):
    with open('/home/matt/repos/advent-2024/15/data.txt') as f:
        map = []
        boxes = []
        r = None
        moves = []
        grid = []
        max_y = 0
        for y, line in enumerate(f):
            l = line.strip()
            l_map = []
            l_boxes = []
            l_grid = []
            for x,c in enumerate(l):
                if version == 2:
                    x = float(x)
                if c == '#':
                    l_map.append(x)
                    l_grid.append("#")
                elif c == 'O':
                    l_boxes.append(x)
                    l_grid.append(".")
                elif c == '@':
                    r = (x,y)
                    l_grid.append(".")
                elif c == '.':
                    l_grid.append(".")
                elif c in ["<",">","^","v"]:
                    moves.append(c)

                if version == 2 and c in ["#",".","O","@"]:
                    l_grid.append(l_grid[-1])

            if line[0] not in ["<",">","^","v"]:
                map.append(l_map)
                boxes.append(l_boxes)
                grid.append(l_grid)
                max_y += 1

    return(map, boxes, moves, r, len(grid[0]), max_y-1, grid)

map, boxes, moves, r, max_x, max_y, grid = get_data()

# room = Room(map, boxes, r, max_x, max_y, grid, 1)
# room.display(False)
# for m in moves:
#     room.move(m)
# room.display(False)

map, boxes, moves, r, max_x, max_y, grid = get_data(2)
room2 = Room(map, boxes, r, max_x, max_y, grid, 2)
room2.display2(False)
c = 0
for m in moves:
    if c == 326:

        next
    room2.move(m)
    c+=1
room2.display2(False)

#print("Q1: {}".format(room.score()))
print("Q2: {}".format(room2.score()))

