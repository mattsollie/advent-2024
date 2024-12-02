from statistics import median
REPORTS = []

def get_data():
    with open('data.txt') as f:
        for line in f:
            REPORTS.append(list(map(int, line.strip().split(' '))))

def analyze_report(report):
    dampened_report = [report[0]]
    dampened = False
    delta = []

    for r in range(1, len(report)):
        sum = report[r] - report[r-1]
        #Q1
        delta.append(sum)
        #Q2 - over max levels
        if (sum < -3 or sum > 3 or sum == 0) and dampened is False:
            print("dampening single error - {}".format(sum))
            dampened = True
        else:
            dampened_report.append(report[r])

    # Q1
    safe = check_safety(delta)
    dampened_delta = []
    for r in range(1, len(dampened_report)):
        sum = dampened_report[r] - dampened_report[r-1]
        dampened_delta.append(sum)

    #If a report has mixed positive and negative we must see if we can fix it    
    if min(dampened_delta) < 0 and max(dampened_delta) > 0:
        # Mixed reports
        rerun = False # We will need to re-run if we remove a bad report here
        if median(dampened_delta) > 0: #This is the only part of this solution I like - determine which is errant against the average of the list
            #Overal Positive report - remove most negative
            print("dampening single negative invese at index - {}".format(dampened_delta.index(min(dampened_delta))))
            dampened_report.pop(dampened_delta.index(min(dampened_delta)))
            rerun = True
        elif median(dampened_report) < 0:
            #Overal Positive report - remove most positive
            print("dampening single negative invese at index - {}".format(dampened_delta.index(max(dampened_delta))))
            dampened_report.pop(dampened_delta.index(max(dampened_delta)))
            rerun = True

        if rerun is True:
            #re-run because we removed an errant level
            dampened_delta = []    
            for r in range(1, len(dampened_report)):
                sum = dampened_report[r] - dampened_report[r-1]
                dampened_delta.append(sum)

    safe_dampened = check_safety(dampened_delta)
    return([safe, safe_dampened, delta])

def check_safety(delta):
    safe = False
    # Negative processing
    if min(delta) >= -3 and max(delta) < 0: # and delta.count(0) == 0:
        safe = True
    # Positive processing
    elif min(delta) > 0 and max(delta) <= 3: # and delta.count(0) == 0:
        safe = True
    else:
        next
    return(safe)


get_data()

r_analysis = []
safe_reports = 0
dampened_reports = 0
for i in range(len(REPORTS)):
    report = analyze_report(REPORTS[i])
    r_analysis.append(report)
    if report[0] == True:
        safe_reports += 1
    if report[1] == True:
        dampened_reports += 1

print("Q1: {}".format(safe_reports))
print("Q2: {}".format(dampened_reports))

