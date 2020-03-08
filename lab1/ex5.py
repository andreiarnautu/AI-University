dictionary = {}
word_list = ["haha", "poc", "Poc", "POC", "haHA", "hei", "hey", "HahA", "poc", "Hei"]

for word in word_list:
    if word.lower() not in dictionary.keys():
        dictionary[word.lower()] = 1
    else:
        dictionary[word.lower()] += 1

for word in dictionary.keys():
    print(word + ": " + str(dictionary[word]))
