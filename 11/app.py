import time

def get_data():
    with open('/home/matt/repos/advent-2024/11/data.txt') as f:
        data = []
        for line in f:
            data.append(line.strip().split(" "))
    return(data[0])

def change_stone(stone, memo):
    if stone not in memo:
        s_stone = str(stone)
        s_len = len(s_stone)
        if stone == 0:
            memo[stone] = [stone + 1]
        elif s_len%2 == 0:
            memo[stone] = [int(s_stone[0:int((s_len/2))]), int(s_stone[int((s_len/2)):])]
        else:
            memo[stone] = [stone * 2024]
    return(memo[stone])

Q1 = 0
memo = {}
count =     {}
all_stones = get_data()
blinks = 75

start_time = time.time()

for ia,stone in enumerate(all_stones):
    stone = int(stone)
    if stone in count.keys():
        count[stone] += 1
    else:
        count[stone] = 1
    local_stones = [stone]

while blinks > 0:
    blinks -= 1
    new_count = {}
    for s in count.keys():
        cur_count = count[s]
        if cur_count >= 1:
            new_stones = change_stone(s, memo)
            for st in new_stones:
                if st in new_count:
                    new_count[st] += cur_count
                else:
                    new_count[st] = cur_count
    count = new_count.copy()

for s in count.keys():
    Q1 += count[s]

print("Length: {}".format(Q1))

end_time = time.time()
dur = round(end_time - start_time, 4)
print("Duration: {}".format(dur))