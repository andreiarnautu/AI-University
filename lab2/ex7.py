##
 #  Worg
 ##


def f1(number_list, n):
    return all([1 if x >= 0 and x % n == 0 else 0 for x in number_list])


def f2(string_list):
    return any([1 if x.isdigit() else 0 for x in string_list])


def f3(matrix):
    return any([0 if any(line) else 1 for line in matrix])


def f4(user_string, word_list):
    return all([x in user_string for x in word_list])


print(f1([18, 22, -32], 2))
print(f2(["abcd", "109b2"]))

matrix = [[0, 2, 0], [1, 0, 2], [3, 2, 4]]
print(f3(matrix))

print(f4("Messi plays football", ["Messi", "soccer"]))
