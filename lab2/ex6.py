##
 #  Worg
 ##
import sys


class Error(Exception):
    """ Base class for other exceptions"""
    pass


class IOError(Error):
    """ Input/output error """
    pass


#
#class ValueError(Error):
#    """ One of the matrix values is not an integer """


class CustomError(Error):
    """ There is not a valid matrix in the input file """



if __name__ == '__main__':
    try:
        file = open("input.txt", "r")
    except Exception:
        print("Could not open input file")
        exit(0)


    try:
        x = 0
        mat = [[int(num) for num in line.split(' ')] for line in file if line.strip() != ""]
    except ValueError:
        print("One of the matrix values is not an integer")
        exit(0)

    try:
        line_size = len(mat[0])
        for line in mat:
            if len(line) != line_size:
                raise CustomError
    except CustomError:
        print("The input doesn't contain a valid matrix")
        exit(0)

    print(mat)
