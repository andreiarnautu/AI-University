# Cerinta 1
l = [10, 2, 12, 1000, 397]
l.sort(key = lambda x : str(x))
print(l)


# Cerinta 2
l.sort(key = lambda x : str(x)[::-1])
print(l)


# Cerinta 3
l.sort(key = lambda x : len(str(x)))
print(l)


# Cerinta 4
l.sort(key = lambda x : len(set(str(x))))
print(l)


# Cerinta 5
l = ["1+2+3","2-5","3+4","5*10"]
l.sort(key = lambda x : eval(x))
print(l)
