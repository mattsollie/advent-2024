import re
import math

def get_data():
    prizes = []
    with open('/home/matt/repos/advent-2024/13/data.txt') as f:
        for line in f:
            l = line.strip()
            if "Button A" in l:
                a = re.search(r'X(\W)(\d+)\, Y(\W)(\d+)',l)
            elif "Button B" in l:
                b = re.search(r'X(\W)(\d+)\, Y(\W)(\d+)',l)
            elif "Prize" in l:
                p = re.search(r': X=(\d+)\, Y=(\d+)',l)
            else:            
                a_loc = (int((a[2])), int((a[4])))
                b_loc = (int((b[2])), int((b[4])))
                p_loc = (int(p[1])+10000000000000,int(p[2])+10000000000000) #Q2
                #p_loc = (int(p[1]),int(p[2])) #Q1
                prizes.append({"a":a_loc, "b":b_loc, "prize":p_loc})
    return(prizes)

games = get_data()
tokens = 0
for game in games:
    p_x, p_y = game['prize'][0], game['prize'][1]
    a_x,a_y = game['a'][0],  game['a'][1]
    b_x, b_y = game['b'][0], game['b'][1]
    b_a = (p_x*b_y - p_y*b_x) / (a_x*b_y - a_y*b_x)
    b_b = (a_x*p_y - a_y*p_x) / (a_x*b_y - a_y*b_x)

    fraca, _ = math.modf(b_a)
    fracb, _ = math.modf(b_b)
    if fraca == 0 and fracb == 0:
        print("  This Game tokens: {}".format((b_a *3) + b_b))
        tokens += int((b_a *3))+ +int(b_b)

print("Q: {}".format(tokens))

