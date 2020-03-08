##
 #  Worg
 ##
import sys

def f1(number_list):
    return {x for x in number_list if str(x)[0] == str(x)[len(str(x)) - 1]}


def f2(matrix):
    return {matrix[i][j] for i in range(0, len(matrix)) for j in range(0, len(matrix[i])) if i == j}



print(f1([122221, 321, 3543, 42]))
matrix = [[0, 2, 3], [1, 6, 9], [3, 9, 3]]
print(f2(matrix))
