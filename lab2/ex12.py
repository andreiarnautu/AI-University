##
 #  Worg
 ##
import sys

def alter_file(file_name):
    fin = open(file_name, 'r+')
    lines = fin.readlines()
    fin.seek(0)
    for line in lines:
        line_result = eval(line)
        fin.write(line[:-1] + "=" + str(line_result) + "\n")
    fin.close()



if __name__ == '__main__':
    alter_file('input_12.txt')

