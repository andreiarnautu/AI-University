# Cerinta 1
def check_equals(number_list):
    return len(set(number_list)) == 1


my_list = [1, 1, 1]
print(check_equals(my_list))


# Cerinta 2
def check_alphabet(word):
    return len(set(word.lower())) == 26


print(check_alphabet("abcdee"))


# Cerinta 3
def check_anagrams(word1, word2):
    return sorted(word1) == sorted(word2)
#    return len(set(word1.lower()) - set(word2.lower())) == 0 and len(set(word2.lower()) - set(word1.lower())) == 0


word1 = "abcd"
word2 = "badc"
print(check_anagrams(word1, word2))


# Cerinta 4
from itertools import chain, combinations

def generate_powerset(elements):
    elem_list = list(elements)
    return set(chain.from_iterable(combinations(elem_list, r) for r in range(len(elem_list) + 1)))

my_set = set("abc")
print(generate_powerset(my_set))


# Cerinta 5
def cartesian_product(m1, m2):
    answer = []
    for x in m1:
        for y in m2:
            answer.append((x, y))
    return answer

a = set("123")
b = set("456")
print(cartesian_product(a, b))
