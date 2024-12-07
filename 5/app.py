Q1 = 0
Q2 = 0

def get_data():
    rules = {}
    updates = []
    with open('data.txt') as f:
        for line in f:
            line = line.strip()
            if "|" in line:
                rule = line.split("|")
                if int(rule[0]) in rules.keys():
                    rules[int(rule[0])].append(int(rule[1]))
                else:
                    rules[int(rule[0])] = [int(rule[1])]
            elif line == "":
                next
            else:
                updates.append([int(x) for x in line.split(",")])
    return(rules,updates)

def test_update(update, rules):
    passing = True
    known_rules = rules.keys()
    for i in range(0, len(update)):
        page = update[i]
        prev_pages = update[0:i]
        if page in known_rules:
            for r in rules[page]:
                if r in prev_pages:
                    passing = False
                    #print("  Fail - {} came after {}".format(page, r))
    return(passing)

def fix_update(update, rules):
    known_rules = rules.keys()
    fixed_update = update.copy()
    attempt = 0
    while not test_update(fixed_update, rules) and attempt < 200:
        attempt += 1
        for i in range(0, len(fixed_update)):
            page = fixed_update[i]
            prev_pages = fixed_update[0:i]
            if page in known_rules:
                for r in rules[page]:
                    if r in prev_pages:
                        #Found Bad Page
                        [print("  Fixing: {} before {}".format(page, r))]
                        fixed_update.remove(page)
                        rule_loc = fixed_update.index(r)
                        fixed_update.insert(rule_loc, page)
            print(" Itterated fix {}: {}".format(i, fixed_update))
    return(fixed_update)

rules,updates = get_data()

for update in updates:
    if test_update(update, rules):
        print("PASSED: {} - middle page: {}".format(update, update[int(len(update)/2)]))
        Q1 += update[int(len(update)/2)]
    else:
        fixed_update = fix_update(update, rules)
        print("FIXED: {} - middle page: {}".format(fixed_update, fixed_update[int(len(update)/2)]))
        Q2 += fixed_update[int(len(fixed_update)/2)]

print("Q1: {}".format(Q1))
print("Q2: {}".format(Q2))

