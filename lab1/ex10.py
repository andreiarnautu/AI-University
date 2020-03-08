##
 #  Worg
 ##

word_list = ["bau-bau", "bobocel", "14 pisici", "1pitic", "pisicel", "botosel", "414", "ham", "-hau", "bob", "bocceluta"]
dictionary = {}

dictionary[(1, 4)] = "mic"
dictionary[(4, 8)] = "mediu"
dictionary[(8, 15)] = "mare"


word_dictionary = {}
for char in range(ord('a'), ord('z') + 1):
    letter = chr(char)
    curr_list = []
    for word in word_list:
        if any(letter in x and len(x) > 1 for x in word.split()):
            curr_list.append(word)

    if len(curr_list) > 0:
        word_dictionary[letter] = curr_list

print(len(word_dictionary))
