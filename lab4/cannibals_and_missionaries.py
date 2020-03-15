##
 #  Worg
 ##
import sys
import copy
from time import time
import bintrees

TOTAL_NO_MISSIONARIES = 3
TOTAL_NO_CANNIBALS = TOTAL_NO_MISSIONARIES
BOAT_SIZE = 2


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
        """ Function that returns the path from the original state to the current node """
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
        heuristic_value = 0

        if self.state[0] == 0:  #  We're on the left side
            heuristic_value = (self.state[1] + self.state[2]) / BOAT_SIZE
        else:
            x = TOTAL_NO_MISSIONARIES - self.state[1]
            y = TOTAL_NO_CANNIBALS - self.state[2]
            heuristic_value = (x + y) / BOAT_SIZE + 1

        return heuristic_value



    def __repr__(self):
        """ Format the node data into something more readable """
        string = "Current state: \n"
        if self.state[0] == 0:  #  We're on the left side
            string += "M: "
            string += str(self.state[1]).ljust(10)
            string += "M: "
            string += str(TOTAL_NO_MISSIONARIES - self.state[1]).ljust(10)
            string += "\n"

            string += "C: "
            string += str(self.state[2]).ljust(10)
            string += "C: "
            string += str(TOTAL_NO_CANNIBALS - self.state[2]).ljust(10)
            string += "\n"

            string += "Boat position: left\n"
        else:  #  We're on the right side
            string += "M: "
            string += str(TOTAL_NO_MISSIONARIES - self.state[1]).ljust(10)
            string += "M: "
            string += str(self.state[1])
            string += "\n"

            string += "C: "
            string += str(TOTAL_NO_CANNIBALS - self.state[2]).ljust(10)
            string += "C: "
            string += str(self.state[2]).ljust(10)
            string += "\n"

            string += "Boat position: right\n"
        string += "\n"
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
        self.moves = []
        for cannibals in range(1, BOAT_SIZE + 1):
            self.moves.append((0, cannibals))
        for missionaries in range(1, BOAT_SIZE + 1):
            for cannibals in range(missionaries + 1):
                if missionaries + cannibals <= BOAT_SIZE:
                    self.moves.append((missionaries, cannibals))


    def expand(self, node : NodeInGraph) -> list:
        """ Function that expands the current node, returning a list of candidate nodes for the next step of the A* algorithm """
        expand_list = []

        for move in self.moves:
            boat_missionaries = move[0]
            boat_cannibals = move[1]

            if node.state[1] < boat_missionaries or node.state[2] < boat_cannibals:
                continue

            x0 = node.state[1] - boat_missionaries
            x1 = TOTAL_NO_MISSIONARIES - x0
            y0 = node.state[2] - boat_cannibals
            y1 = TOTAL_NO_CANNIBALS - y0

            if (x0 < y0 and x0 > 0) or (x1 < y1 and x1 > 0):
                continue

            new_state = (1 - node.state[0], x1, y1)
            next_node = NodeInGraph(new_state, node)
            expand_list.append(next_node)

        return expand_list


def astar_search(graph : Graph):
    open_nodes = bintrees.RBTree()
    fg_values = bintrees.RBTree()

    #  Create the start and end nodes
    end_node = NodeInGraph(graph.end_config, None)

    start_node = NodeInGraph(graph.start_config, None)
    start_node.g = 0
    start_node.h = start_node.compute_heuristic(end_node)
    start_node.f = start_node.g + start_node.h

    open_nodes[start_node] = 0  #  start node's g value
    fg_values[start_node.state] = (start_node.f, start_node.g)

    max_states = 0
    while len(open_nodes) > 0:
        max_states = max(max_states, len(open_nodes))
        current_node = open_nodes.pop_min()[0]

        #  Check for the node being None
        if current_node is None:
            print("Error: current node is None.")
            exit(0)

        #  Check if we reached the goal state and return the path
        if current_node.state == end_node.state:
            print("Total number of states ever added: " + str(len(fg_values)))
            print("Maximum number of states in the open set at a certain point: " + str(max_states))
            print("Moves used: " + str(current_node.moves_used))
            return current_node.get_path()

        #  Get neighbours, then iterate through them
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
                #  Make an artificial node to see if the current state exists in the open set.
                #  We don't want the same state to exist in the open set with different f values.
                #  We only want to keep the instance with the smallest f value.
                aux_node = NodeInGraph(next_node.state, None)
                aux_node.f = fg_values[next_node.state][0]

                fg_values[next_node.state] = (next_node.f, next_node.g)
                if open_nodes.__contains__(aux_node) == False:
                    open_nodes[next_node] = next_node.g
                else:
                    open_nodes.remove(aux_node)
                    open_nodes[next_node] = next_node.g

    print("No solutions found. Total number of states visited is: " + str(max_states) + ".")
    return None


if __name__ == "__main__":
    t0 = time()

    start_config = (0, TOTAL_NO_MISSIONARIES, TOTAL_NO_CANNIBALS)
    end_config = (1, TOTAL_NO_MISSIONARIES, TOTAL_NO_CANNIBALS)
    graph = Graph(start_config, end_config)

    result = astar_search(graph)
    print(result)

    t1 = time()
    print("Execution took " + str(round(t1 - t0, 6)) + " seconds.")
