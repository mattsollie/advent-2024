Q = 0

def get_data():
    math = []
    with open('data.txt') as f:
        for line in f:
            p = line.strip().split(": ")
            math.append({"answer": p[0], "numbers": [int(i) for i in p[1].split(" ")]})
    return(math)

math = get_data()

for problem in math:
    answer = int(problem["answer"])
    answers = [problem["numbers"][0]]
    for i in range(0,len(problem["numbers"])-1):
        tmp = []
        for t in answers:
            a = t + problem["numbers"][i+1]
            m = t * problem["numbers"][i+1]
            #Q1
            #mp += [a,m]
            #Q2
            c = int("".join([str(t),str(problem["numbers"][i+1])]))
            tmp += [a,m,c]
        answers = tmp
    if answer in answers:
        Q += answer

print("Q: {}".format(Q))