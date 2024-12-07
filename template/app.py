Q1 = 0
Q2 = 0

def get_data():
    with open('data.txt') as f:
        data = []
        for line in f:
            data.append(line.strip())
    return(data)


data = get_data()

print("Q1: {}".format(Q1))
print("Q2: {}".format(Q2))