##
 #  Worg
 ##
import sys


def parse_file(file_name):
    fin = open(file_name, "r")
    l1 = []
    l2 = []
    l3 = []
    for line in fin:
        word_list = line.split(' ')

        for word in word_list:
            flag = True
            try:
                l1.append(int(word))
                flag = False
            except Exception:
                flag = True
                pass

            if flag == True:
                try:
                    l2.append(float(word))
                    flag = False
                except Exception:
                    flag = True
                    pass

            if flag == True:
                l3.append(word)

    fin.close()
    return (l1, l2, l3)



if __name__ == '__main__':
    print(parse_file("input_11.txt"))
