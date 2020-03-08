##
 #  Worg
 ##
import sys

class Error(Exception):
    """ Base class for other exceptions"""
    pass


class ColumnDirError(Error):
    """Raised when one element of the tuple is too long"""
    pass


class ListArgumentError(Error):
    """Raised when one of the tuples is not valid"""


class GenericArgumentError(Error):
    """ The parameters of the function are not valid"""
    pass


sep_character = " "

def print_on_two_columns(column_size, tuples):
    try:
        if (not type(column_size) == int) or (not type(tuples) == list):
            raise GenericArgumentError
        for x in tuples:
            if not type(x) == tuple or not len(x) == 2:
                raise ListArgumentError
        for x in tuples:
            for y in x:
                if len(str(y)) > column_size:
                    raise ColumnDirError
    except GenericArgumentError:
        print("Error: the parameters of the function are not valid")
        exit(0)
    except ListArgumentError:
        print("Error: at least one of the tuples is not valid")
    except ColumnDirError:
        print("Error: an element of the tuple is too long")
        exit(0)

    for curr_tuple in tuples:
        for element in curr_tuple:
            print(str(element).ljust(column_size, " "), end = " ")
        print()


def print_on_three_columns(column_size, tuples):
    try:
        if type(column_size) != int or type(tuples) != list:
            raise GenericArgumentError
        for curr_tuple in tuples:
            if type(curr_tuple) != tuple or len(curr_tuple) != 3:
                raise ListArgumentError
        for curr_tuple in tuples:
            for element in curr_tuple:
                if len(str(element)) > column_size:
                   raise ColumnDirError
    except GenericArgumentError:
        print("Error: the parameters of the function are not valid")
        exit(0)
    except ListArgumentError:
        print("Error: at least one of the tuples is not valid")
    except ColumnDirError:
        print("Error: an element of the tuple is too long")
        exit(0)

    for curr_tuple in tuples:
        i = 0
        for element in curr_tuple:
            if (i < 2):
                print(str(element).center(column_size, " "), end = sep_character)
            else:
                print(str(element).center(column_size, " "), end = "\n")
            i += 1

