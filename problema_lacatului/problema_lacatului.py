##
 #  Worg
 ##
import sys
import copy
from time import time
import bintrees

INF = 10**9  #  constant variable

'''  Class containing the info about a node in the search tree '''
class NodeInGraph:
    def __init__(self, state, parent, key_used = None):
        self.state = state
        self.parent = parent
        self.g = INF  #  Distance to start node
        self.h = INF  #  Distance to end node
        self.f = INF  #  Total distance (h + g)
        self.moves_used = 0
        self.key_used = key_used


    '''  Function that returns the path from the original state to the current one '''
    def get_path(self):
        pass


    ''' Format the node data into something more readable '''
    def __repr__(self):
        pass

    def __eq__(self, other):
        return self.f == other.f and self.state == other.state


    def __lt__ (self, other):
        return (self.f < other.f) or (self.f == other.f and self.state < other.state)


    def __le__(self, other):
        return self == other or self < other


'''  Class containing the info about the problem graph and some needed functions in it '''
class Graph:
    pass


'''  Max value in the state array '''
def heurstic_1(node : NodeInGraph):
    value = 0
    for x in node.state:
        value = max(value, x)
    return value


'''  Average value in the state array '''
def heuristic_2(node : NodeInGraph):
    value = 0
    for x in node.state:
        value += x
    return value / len(node.state)


'''  Sum of the values in the state array - not an admissible heuristic '''
def heuristic_3(node : NodeInGraph):
    value = 0
    for x in node.state:
        value += x
    return value



if __name__ == '__main__':
    t0 = time()
    start_config = ''
    end_config = ''

