text = "Candva, demult, acum 1000 de ani traia o printesa intr-un castel. Si printesa intr-o zi auzi cum aparuse pe meleagurile sale un cufar fermecat din care iesea grai omenesc. Printesa curioasa strabatu 7 ulite si 7 piete; ajunse la cufar si vazu ca toti stateau la 100 metri distanta de el si se mirau. Din cufar intr-adevar se auzeau vorbe nedeslusite. Printesa curajoasa se duse sa-i vorbeasca. Il intreba cine e si ce dorinte are. Raspunsul fu: \"Sunt Ion am cazut in cufar si m-am ferecat din gresala. As dori sa ies.\". Printesa deschise cufarul si-l elibera pe Ion. \"Multumesc\" spuse Ion. Si astfel, povestea cufarului fermecat a fost deslusita."


def get_non_alphanumeric(text):
    char_list = ""
    for c in text:
        if not c.isalnum():
            if not c in char_list and c != '-':
                char_list = char_list + c
    return char_list


def get_word_list(text, separator_list):
    word_list = text.split(separator_list[0])

    for i in range(1, len(separator_list)):
        new_word_list = []
        for word in word_list:
            aux_list = word.split(separator_list[i])
            if '' in aux_list:
                aux_list.remove('')
            new_word_list = new_word_list + aux_list
        word_list = new_word_list

    return word_list


def get_special_words(word_list: list):
    special_words = []
    for word in word_list:
        if word.endswith('ul'):
            special_words.append(word)
    return special_words



def get_line_words(word_list):
    line_words = []
    for word in word_list:
        if '-' in word:
            line_words.append(word)
    return line_words


print(len(text))
separator_list = get_non_alphanumeric(text)
print(separator_list)
word_list = get_word_list(text, separator_list)
print(word_list)

words_m = get_special_words(word_list)
print(words_m)

line_words = get_line_words(word_list)
print(line_words)

