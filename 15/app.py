from time import sleep
Q1, Q2 = 0, 0

class Room:
    def __init__ (self, map, boxes, robot, max_x, max_y, grid):
        #self.position = robot
        self.pos_x = robot[0]
        self.pos_y = robot[1]
        self.map = map
        self.boxes = boxes
        self.max_x = max_x
        self.max_y = max_y
        self.grid = grid

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

    def score(self):
        score = 0
        for n, r in enumerate(self.boxes):
            for b in r:
                score += (100 * n) + b
        return(score)

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

        print("  Move {} to {}".format(self.pos_x, self.pos_x + x))
        if x != 0:
            if (self.pos_x + x) in self.map[self.pos_y]: # wall - skip
                print("    Hit Wall")
            elif (self.pos_x + x) not in self.map[self.pos_y] and (self.pos_x + x) not in self.boxes[self.pos_y]: #Open position
                print("    Open location")
                self.pos_x = self.pos_x + x
            elif (self.pos_x + x) not in self.map[self.pos_y] and (self.pos_x + x) in self.boxes[self.pos_y]: #no wall, but a box
                print("    Box location")
                found = False
                s = self.pos_x + x
                while found == False and s > 0 and s < max_x:
                    if s in self.map[self.pos_y]:
                        break
                    if s not in self.map[self.pos_y] and s not in self.boxes[self.pos_y]:
                        found = True
                        print(s)
                    else:
                        s += x
                if found:
                    print("    blocked spaces from {} to {}. Next Open space {}".format(self.pos_x + x, s-1, s))
                    if x>0:
                        positions = list(range(self.pos_x + x, s))
                    else:
                        positions = list(range(s, self.pos_x))
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
            boxes = [i for i, x in enumerate(self.boxes) if self.pos_x in x]
            walls = [i for i, x in enumerate(self.map) if self.pos_x in x]
        
            if (self.pos_y + y) in walls: # wall - skip
                print("   Hit Wall")
            elif (self.pos_y + y) not in  walls and (self.pos_y + y) not in boxes: #Open position
                print("   Open location")
                self.pos_y = self.pos_y + y
            elif (self.pos_y + y) not in  walls and (self.pos_y + y) in boxes: #no wall, but a box
                print("    Blocked location")
                print(" Column {}".format(boxes))
                found = False
                s = self.pos_y + y
                while found == False and s > 0 and s < max_y:
                    if s in walls:
                        break
                    elif s not in walls and s not in boxes:
                        found = True
                        print(s)
                    else:
                        s += y
                if found:
                    print("blocked spaces from {} to {}. Next Open space {}".format(self.pos_y + y, s-1, s))
                    if y>0:
                        positions = list(range(self.pos_y + y, s))
                    else:
                        positions = list(range(s, self.pos_y))
                    positions.sort(reverse=y>0)
                    print("will check positions {}".format(positions))
                    for i in positions:
                        if i in boxes:
                            print("move {} by {}".format(i, y))
                            self.boxes[i+y].append(self.boxes[i].pop(self.boxes[i].index(self.pos_x)))
                    print(" Column {}".format(boxes))
                    self.pos_y = self.pos_y + y
                else:
                    print("no free space found")


                
                    

def get_data():
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


            if line[0] not in ["<",">","^","v"]:
                map.append(l_map)
                boxes.append(l_boxes)
                grid.append(l_grid)
                max_y += 1
    return(map, boxes, moves, r, len(grid[0]), max_y-1, grid)

map, boxes, moves, r, max_x, max_y, grid = get_data()

room = Room(map, boxes, r, max_x, max_y, grid)
room.display(False)
for m in moves:
    room.move(m)
room.display(False)

print("Q1: {}".format(room.score()))
print("Q2: {}".format(Q2))

