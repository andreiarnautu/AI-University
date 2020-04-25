##
 #  Worg
 ##
import sys
import copy
from time import time
import bintrees

INF = 10**9  #  constant variable

def char_to_number(ch):
    if ch == 'd':
        return 0
    elif ch == 'i':
        return 1
    elif ch == 'g':
        return -1
    else:
        print('The character given as a parameter is not d/g/i.')
        sys.exit(0)


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
        node_list = []
        node = self
        while node is not None:
            node_list.append(node)
            node = node.parent
        return node_list[::-1]


    ''' Format the node data into something more readable '''
    def __repr__(self):
        string = '['
        for i in range(len(self.state)):
            if self.state[i] == 0:
                string += 'd'
            else:
                string += 'i' + str(self.state[i])

            if i + 1 < len(self.state):
                string += ', '
            else:
                string += ']'
        return string


    def __eq__(self, other):
        return self.f == other.f and self.state == other.state


    def __lt__ (self, other):
        return (self.f < other.f) or (self.f == other.f and self.state < other.state)


    def __le__(self, other):
        return self == other or self < other


'''  Class containing the info about the problem graph and some needed functions in it '''
class Graph:
    def __init__(self, start_config, end_config, key_list):
        self.start_config = start_config
        self.end_config = end_config
        self.key_list = key_list
        self.size = len(start_config)


    '''  Function that expands the current node, returning a list of candidate nodes for the next step of the A* algorithm '''
    def expand(self, node : NodeInGraph) -> list:
        expand_list = []
        for key in self.key_list:
            #  Apply the current key
            state_copy = copy.deepcopy(node.state)
            for i in range(len(key)):
                if key[i] == 'g':
                    continue
                elif key[i] == 'i':
                    state_copy[i] += 1
                elif key[i] == 'd':
                    state_copy[i] = max(0, state_copy[i] - 1)
            next_node = NodeInGraph(state_copy, node, key)
            expand_list.append(next_node)
        return expand_list


'''  Max value in the state array '''
def heuristic_1(node : NodeInGraph):
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


'''  Run A* algorithm on a given graph while using a certain heuristic '''
def astar_search(graph : Graph, heuristic, file_descriptor):
    open_nodes = bintrees.AVLTree()
    fg_values = bintrees.AVLTree()

    #  Create the start and end node
    end_node = NodeInGraph(graph.end_config, None)

    start_node = NodeInGraph(graph.start_config, None)
    start_node.g = 0
    start_node.h = heuristic(start_node)
    start_node.f = start_node.g + start_node.h

    open_nodes[start_node] = 0  #  start node's g value
    fg_values[start_node.state] = (start_node.f, start_node.g)

    max_states = 0
    while len(open_nodes) > 0:
        max_states = max(max_states, len(open_nodes))
        current_node = open_nodes.pop_min()[0]

        #  Check for the node being None
        if current_node is None:
            print('Error: current node is None.')
            sys.exit(0)

        #  Check if we reached the goal state and return the path
        if current_node.state == end_node.state:
            file_descriptor.write('Total number of states ever visited: ' + str(len(fg_values)) + '\n')
            file_descriptor.write('Maximum number of states in the open set at any certain point: ' + str(max_states) + '\n')
            file_descriptor.write('Moves used: ' + str(current_node.moves_used) + '\n')
            return current_node.get_path()

        #  Get neighbours
        neighbours = graph.expand(current_node)
        for next_node in neighbours:
            next_node.g = current_node.g + 1
            next_node.h = heuristic(next_node)
            next_node.f = next_node.g + next_node.h

            if fg_values.__contains__(next_node.state) == False:
                fg_values[next_node.state] = (next_node.f, next_node.g)  #  Add it to fg_values
                open_nodes[next_node] = next_node.g  #  Add it to the open set
            elif next_node.g < fg_values[next_node.state][1]:
                #  Make an artificial node to see if the current state exists in the open set
                #  We don't want the same state to exist in the open set with different f values
                #  We only want to keep the instance with the smallest f value
                aux_node = NodeInGraph(next_node.state, None)
                aux_node.f = fg_values[next_node.state][0]

                fg_values[next_node.state] = (next_node.f, next_node.g)
                if open_nodes.__contains__(aux_node) == False:
                    open_nodes[next_node] = next_node.g
                else:
                    open_nodes.remove(aux_node)
                    open_nodes[next_node] = next_node.g

    file_descriptor.write('No solutions found. Total number of states is ' + str(max_states) + '.\n')
    return None


'''  Function that returns a string that describes a given key '''
def prettify_key(key):
    string = '['
    for i in range(len(key)):
        string += key[i]
        if i + 1 < len(key):
            string += ', '
        else:
            string += ']'
    return string


'''  Function that prints the output in a given file '''
def print_path(path, file_descriptor):
    line_id = 0

    for node in path:
        file_descriptor.write(str(line_id) + '. ')
        if node.key_used is None:
            file_descriptor.write('Starting state: ' + str(node) + '\n')
        else:
            file_descriptor.write('Used key ' + prettify_key(node.key_used) + '. Current state: ' + str(node) + '\n')
        line_id += 1


'''  Function that fetches the keys from an input file '''
def get_keys(file_descriptor):
    key_list = []
    for line in file_descriptor.readlines():
        key = line.split(sep = '\n')[0]
        key_list.append(key)
    return key_list


if __name__ == '__main__':
    lock_size = int(sys.argv[1])
    file_descriptor = open(sys.argv[2], 'r')
    key_list = get_keys(file_descriptor)
    file_descriptor.close()

    #  Check condition
    for i in range(lock_size):
        ok = False
        for key in key_list:
            if key[i] == 'd':
                ok = True

        if ok is False:
            print('The given set of keys cannot open the lock.')
            sys.exit(0)


    start_config = [1 for i in range(lock_size)]
    end_config = [0 for i in range(lock_size)]
    graph = Graph(start_config, end_config, key_list)

    #  First heuristic
    t0 = time()
    file_descriptor = open('heuristic_1.txt', 'w')
    path = astar_search(graph, heuristic_1, file_descriptor)
    if path is not None:
        print_path(path, file_descriptor)
    t1 = time()
    file_descriptor.write('Execution took ' + str(int(1000 * (t1 - t0))) + ' ms.\n')
    file_descriptor.close()

    #  Second heuristic
    t0 = time()
    file_descriptor = open('heuristic_2.txt', 'w')
    path = astar_search(graph, heuristic_2, file_descriptor)
    if path is not None:
        print_path(path, file_descriptor)
    t1 = time()
    file_descriptor.write('Execution took ' + str(int(1000 * (t1 - t0))) + ' ms.\n')
    file_descriptor.close()

    #  Third heuristic
    t0 = time()
    file_descriptor = open('heuristic_3.txt', 'w')
    path = astar_search(graph, heuristic_3, file_descriptor)
    if path is not None:
        print_path(path, file_descriptor)
    t1 = time()
    file_descriptor.write('Execution took ' + str(int(1000 * (t1 - t0))) + ' ms.\n')
    file_descriptor.close()

