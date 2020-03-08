##
 #  Worg
 ##

def f1(n1, n2):
    return {x : [y for y in range(1, x + 1) if x % y == 0] for x in range(n1 + 1, n2)}


def f2(list_of_lists):
    return {sum(x) : tuple(x) for x in list_of_lists}


def f3(list_of_tuples):
    return {x : [y for y in range(min(x), max(x)) if not y in x] for x in list_of_tuples}

print(f1(1, 15))
l = [[1, 2, 3], [4, 5, 6], [5, 0, 1]]
print(f2(l))

lt = [(3,7,9),(1,2,3,4),(10,3,5,6),(2,2),(6,7,1,2,4)]
print(f3(lt))
