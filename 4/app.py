import re
Q1 = 0
Q2 = 0

def get_data():
    with open('data.txt') as f:
        data = []
        for line in f:
            data.append(line.strip())
    return(data)

def rotate_matrix(matrix, count=1):
    """rotate 90 degrees * count"""
    for i in range(0,count):
        new_matrix = list(zip(*matrix[::-1]))
        for i in range(len(matrix)):
            matrix[i] = "".join(new_matrix[i])
    print(" -- rotated")
    return(matrix)
        
def angle_matrix(matrix, reverse = False, rotate=True):
    matrix = matrix.copy()
    for i in range(len(matrix)):
        if reverse:
            matrix[i] = ("." * (len(matrix) - i)) + matrix[i] + ("." * i)
        else:
            matrix[i] = ("." * i) + matrix[i] + ("." * (len(matrix) - i)) 
    width = len(matrix[0])
    for i in range(width - len(matrix)):
        matrix.append(("." * width))
    if rotate is True:
        matrix = rotate_matrix(matrix)
    return(matrix)

def print_matrix(m):
    for i in range(len(m)):
        print(m[i])
    print("----")

def search_matrix(matrix, reverse=True):
    count = 0
    for i in range(len(matrix)):
        print("searching {}: {}".format(i, matrix[i]))
        for m in re.finditer(r'XMAS', matrix[i]):
            count += 1
            print(" f: {}".format(m))
    if reverse:
        for i in range(len(matrix)):
            matrix[i] = matrix[i][::-1]
        for i in range(len(matrix)):
            print("searching {}: {}".format(i, matrix[i]))
            for m in re.finditer(r'XMAS', matrix[i]):
                count += 1
                print(" r: {}".format(m))
        for i in range(len(matrix)):
            matrix[i] = matrix[i][::-1]
    print(count)
    return(count)

def check_corners(matrix, loc, i):
    try:
        corners = [[matrix[i-1][loc-1],matrix[i+1][loc+1]],[matrix[i-1][loc+1],matrix[i+1][loc-1]]]
        if corners[0].count('S') == 1 and corners[0].count('M') == 1 and corners[1].count('S') == 1 and corners[1].count('M') == 1:
            return(True)
        else:
            return(False)
    except IndexError: 
        return(False)

def search_matrix_2(matrix):
    count = 0
    for i in range(1, len(matrix)-1):
        for m in re.finditer(r'A', matrix[i]):
            if check_corners(matrix, m.span()[0], i):
                count += 1
    return(count)

matrix = get_data()
#Q1 - Up and Down
print("Question 1")
Q1 += search_matrix(matrix)
rotate_matrix(matrix, 1)
Q1 += search_matrix(matrix)
rotate_matrix(matrix, 3)

#Q1 Diagonal
diag_matrix_1 = angle_matrix(matrix, False)
print_matrix(diag_matrix_1)
Q1 += search_matrix(diag_matrix_1, True)
diag_matrix_2 = angle_matrix(matrix, True)
Q1 += search_matrix(diag_matrix_2, True)
print("End Question 1")

#Q2
print("Question 2")
Q2 = search_matrix_2(matrix)

print("Q1: {}".format(Q1))
print("Q2: {}".format(Q2))

