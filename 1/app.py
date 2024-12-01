q1 = 0
q2 = 0
START = []
END = []
def get_data():
    with open('data.txt') as f:
        for line in f:
            line = line.strip().split('   ')
            START.append(int(line[0]))
            END.append(int(line[1]))

get_data()
#q2
for i in range(len(START)):
    count = 0
    try:
        count = END.count(START[i])
    except:
        count = 0
    q2 += START[i] * count  

#q1
START.sort()        
END.sort()
for i in range(len(START)):
    a = abs(END.pop(0) - START.pop(0))
    q1 += a

print("Q1: {}".format(q1))
print("Q2: {}".format(q2))

