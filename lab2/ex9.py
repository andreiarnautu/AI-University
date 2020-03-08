##
 #  Worg
 ##
import sys

def f1(n):
    return [[y for y in range(1, n + 1)] for x in range(n)]


def f2(matrix):
    return [x[::-1] for x in matrix]




print(f1(4))
matrix = [[0, 2, 3], [1, 4, 7], [6, 2, 5]]
print(f2(matrix))

# ---------------- Task 3 ----------------
class Error(Exception):
    """ Base class for other exceptions """
    pass


class NotValidMatrix(Error):
    """ A given matrix is not valid """
    pass


class DifferentSizes(Error):
    """ Two matrices have different sizes """
    pass


def f3(m1, m2):
    answer = []
    try:
        if len(m1) != len(m2):
            raise DifferentSizes
        row_len = -1
        for (row1, row2) in zip(m1, m2):
            if len(row1) != len(row2):
                raise DifferentSizes
            if row_len != -1 and len(row1) != row_len:
                raise NotValidMatrix
            row_len = len(row1)

            answer.append([row1[i] if ord(row1[i]) < ord(row2[i]) else row2[i] for i in range(len(row1))])

    except NotValidMatrix:
        print("Error: One of the matrices is not valid.")
        exit(0)
    except DifferentSizes:
        print("Error: The matrices have different sizes.")
        exit(0)

    return answer

m1 = [['a', 'b', 'c'], ['d', 'e', 'f'], ['a', 'e', 'c']]
m2 = [['d', 'e', 'f'], ['a', 'b', 'c'], ['d', 'b', 'f']]
print(f3(m1, m2))

# ---------------- Task 4 ----------------
def f4(n):
    return [[0 if i == j else 1 if i < j else -1 for j in range (0, n)] for i in range(0, n)]

print(f4(5))

# ---------------- Task 5 ----------------
def f5(l1, l2):
    return [[0 if l1[x] % 2 == l2[y] % 2 else 1 for y in range(len(l2))] for x in range(len(l1))]


l1 = [1, 2, 3, 4, 5]
l2 = [2, 3, 4, 5, 6]
print(f5(l1, l2))
