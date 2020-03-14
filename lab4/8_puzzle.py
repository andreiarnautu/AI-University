##
 #  Worg
 ##
import sys
import copy
from time import time
import bintrees

class NodeInGraph:
    """  Class containing the info about a node in the search tree """

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.g = 10**9  #  Distance to start node
        self.h = 10**9  #  Predicted distance to end node
        self.f = 10**9  #  Total distance (h + g)
        self.moves_used = 0

    def get_path(self):
        """ Function that returns the path from the original state to the current one """
        node_list = []
        node = self
        while node is not None:
            node_list.append(node)
            node = node.parent

        path = ""
        for i in range(len(node_list) - 1, -1, -1):
            path += node_list[i].__repr__()
        return path


    def compute_heuristic(self, end_node):
        """ The sum of manhattan distances """
        curr_place = {}
        for i in range(len(self.state)):
            if self.state[i] != '#':
                curr_place[self.state[i]] = (i / 3, i % 3)

        heuristic_value = 0
        for i in range(len(self.state)):
            if end_node.state[i] != '#':
                x = end_node.state[i]
                heuristic_value += abs(curr_place[x][0] - i / 3) + abs(curr_place[x][1] - i % 3)
        return heuristic_value


    def __repr__(self):
        """ Format the node data into something more readable """
        string = "Current state: \n"
        for i in range(0, 7, 3):
            string += self.state[i] + " " + self.state[i + 1] + " " + self.state[i + 2] + "\n"
        return string


    def __eq__(self, other):
        return self.f == other.f and self.state == other.state


    def __lt__(self, other):
        return (self.f < other.f) or (self.f == other.f and self.state < other.state)


    def __le__(self, other):
        return self == other or self < other


class Graph:
    """ Class containing the info about the problem graph and some needed functions on it """

    def __init__(self, start_config, end_config):
        self.start_config = start_config
        self.end_config = end_config
        self.size = len(start_config)
        #  Harcode the possible moves
        self.moves = {}
        self.moves[0] = [1, 3]
        self.moves[1] = [0, 2, 4]
        self.moves[2] = [1, 5]
        self.moves[3] = [0, 4, 6]
        self.moves[4] = [1, 3, 5, 7]
        self.moves[5] = [2, 4, 8]
        self.moves[6] = [3, 7]
        self.moves[7] = [4, 6, 8]
        self.moves[8] = [5, 7]


    def expand(self, node : NodeInGraph) -> list:
        """ Function that expands the current node, returning a list of candidate nodes for the next step of the A* algorithm """
        expand_list = []

        for i in range(self.size):
            if node.state[i] == '#':
                state_copy = copy.deepcopy(node.state)
                aux_node = NodeInGraph(state_copy, node)

                for move in self.moves[i]:
                    state_new = copy.deepcopy(aux_node.state)
                    state_new = list(state_new)
                    state_new[i] = node.state[move]
                    state_new[move] = '#'
                    state_new = "".join(state_new)

                    next_node = NodeInGraph(state_new, node)
                    expand_list.append(next_node)
        return expand_list


def astar_search(graph : Graph):
    open_nodes = bintrees.AVLTree()
    fg_values = bintrees.AVLTree()

    #  Create the start and end node
    end_node = NodeInGraph(graph.end_config, None)

    start_node = NodeInGraph(graph.start_config, None)
    start_node.g = 0
    start_node.h = start_node.compute_heuristic(end_node)
    start_node.f = start_node.g + start_node.h

    open_nodes[start_node] = 0  #  start node's g value
    fg_values[start_node.state] = (start_node.f, start_node.g)

    max_states = 0
    while len(open_nodes) > 0:
        max_states = max(max_states, open_nodes.__len__())
        current_node = open_nodes.pop_min()[0]

        #  Check for the node being None
        if current_node is None:
            print("Error: current node is None.")
            exit(0)

        #  Check if we reached the goal state and return the path
        if current_node.state == end_node.state:
            print("Total number of states ever visited: " + str(fg_values.__len__()))
            print("Maximum number of states in the open set at a certain point: " + str(max_states))
            print("Moves used: " + str(current_node.moves_used))
            return current_node.get_path()

        #  Get neighbours
        neighbours = graph.expand(current_node)
        for next_node in neighbours:
            next_node.g = current_node.g + 1
            next_node.h = next_node.compute_heuristic(end_node)
            next_node.f = next_node.g + next_node.h
            next_node.moves_used = current_node.moves_used + 1

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

    print("No solutions found. Total number of states is " + str(max_states))
    return None




if __name__ == '__main__':
    t0 = time()

    start_config = "64785#321"
    end_config = "12345678#"
    graph = Graph(start_config, end_config)

    result = astar_search(graph)
    print(result)

    t1 = time()
    print("Execution took " + str(round(1000 * (t1 - t0), 2)) + " ms.")
