##
 #  Worg
 ##


# Cerinta 1
l1 = [x for x in range(1, 11, 2)]
print(l1)


# Cerinta 2
l2 = [chr(x) for x in range(ord('a'), ord('z') + 1)]
print(l2)


# Cerinta 3
def f1(n):
    l = [x * (-1) ** (x + 1) for x in range(1, n + 1)]
    return l


print(f1(5))


# Cerinta 4
def f2(number_list):
    l = [x for x in number_list if x % 2 == 1]
    return l


print(f2([24, 13, 3, 1, 90, 5, 8, 6, 2, 7]))


# Cerinta 5
def f3(number_list):
    l = [number_list[x] for x in range(0, len(number_list), 2)]
    return l


print(f3([0, 1, 2, 3, 4, 5, 6]))


# Cerinta 6
def f4(number_list):
    l = [number_list[x] for x in range(0, len(number_list)) if x % 2 == number_list[x] % 2]
    return l

print(f4([2,4,1,7,5,1,8,10]))


# Cerinta 7
def f5(number_list):
    l = [(number_list[x], number_list[x + 1]) for x in range(0, len(number_list) - 1)]
    return l


print(f5([5, 6, 7, 8]))


# Cerinta 8
def f6(n):
    l = [["{} * {} = {}".format(x, y, x * y) for y in range(1, n + 1)] for x in range(1, n + 1)]
    return l


print(f6(5))


# Cerinta 9
def f7(user_string):
    l = [(user_string[i:] + user_string[:i]) for i in range(0, len(user_string))]
    return l


print(f7("abcde"))


# Cerinta 9
def f8(n):
    l = [[x for y in range(0, x)] for x in range(0, n)]
    return l


print(f8(5))
