##
 #  Worg
 ##
import sys
import copy
import psutil
from time import time
import bintrees  #  Magic


class NodeInGraph:
    """  Class containing the info about a node in the search tree """

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.g = 10**9  #  Distance to start node
        self.h = 10**9  #  Distance to end node
        self.f = 10**9  #  Total distance


    def get_path(self):
        """ Function that returns the path from the original state to the current one """
        node_list = []
        node = self
        while node is not None:
            node_list.append(node)
            node = node.parent

        path = ""
        for i in range(len(node_list) -1, -1, -1):
            path += node_list[i].__repr__()
        return path


    def compute_heuristic(self, end_node):
        heuristic_cost = 0

        my_dict = {}
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                my_dict[self.state[i][j]] = (i, j)

        for i in range(len(end_node.state)):
            for j in range(len(end_node.state[i])):
                if i != my_dict[end_node.state[i][j]][0]:
                    heuristic_cost += j + my_dict[end_node.state[i][j]][1]
                else:
                    heuristic_cost += abs(j -  my_dict[end_node.state[i][j]][0])
        return heuristic_cost


    def __repr__(self):
        """ Format the node data into something readable """
        string = "State (top of each stack is at the left):\n"

        stack_list = []
        for i in range(len(self.state)):
            stack_string = "["
            for j in range(len(self.state[i])):
                stack_string += str(self.state[i][j])
                if j < len(self.state[i]) - 1:
                    stack_string += " "
            stack_string += "]\n"
            stack_list.append(stack_string)


        for stack_string in stack_list:
            string += stack_string
        string += "\n"
        return string


    def __eq__(self, other):
        return self.f == other.f and self.state == other.state

    def __lt__(self, other):
        return (self.f < other.f) or (self.f == other.f and self.state < other.state)

    def __le__(self, other):
        return self == other or self < other


class Graph:
    """ Class containing info about the problem graph. Note that at no given moment will the whole graph data be stored """

    def __init__(self, start_config, end_config):
        self.start_config = start_config
        self.end_config = end_config
        self.size = len(start_config)


    def expand(self, node : NodeInGraph) -> list:
        """  Function that expands the current node, returning a list of candidate nodes for the next step of the A* algorithm """
        expand_list = []

        for i in range(self.size):
            #  Try to move the top of the i-th stack
            if len(node.state[i]) > 0:
                state_copy = copy.deepcopy(node.state)
                aux_node = NodeInGraph(state_copy, node)
                element = aux_node.state[i].pop(0)

                for j in range(self.size):
                    if i != j:
                        state_new = copy.deepcopy(aux_node.state)
                        next_node = NodeInGraph(state_new, node)
                        next_node.state[j].insert(0, element)
                        expand_list.append(next_node)
        return expand_list


def astar_search(graph: Graph):
    open_nodes = bintrees.AVLTree()
    fg_values = bintrees.AVLTree()

    #  Create the start and end node
    end_node = NodeInGraph(graph.end_config, None)

    start_node = NodeInGraph(graph.start_config, None)
    start_node.g = 0
    start_node.h = start_node.compute_heuristic(end_node)
    start_node.f = start_node.g + start_node.h

    open_nodes[start_node] = 0  #  start_node's g value
    fg_values[start_node.state] = (start_node.f, start_node.g)

    max_states = 0
    while len(open_nodes) > 0:
        max_states = max(max_states, open_nodes.__len__())
        current_node = open_nodes.pop_min()[0]
        #  Check if we reached the goal and return the path
        if current_node is None:
            print("Error: current node is None.")
            exit(0)

        if current_node.state == end_node.state:
            print("Total number of states ever visited: " + str(fg_values.__len__()))
            print("Maximum number of states in the open set at a certain point: " + str(max_states))
            return current_node.get_path()


        #  Get neighbours
        neighbours = graph.expand(current_node)

        for next_node in neighbours:
            next_node.g = current_node.g + 1
            next_node.h = next_node.compute_heuristic(end_node)
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

    return None

if __name__ == "__main__":
    t0 = time()
    start_config = [["a"], ["b", "c"], ["d"]]
    end_config = [["c", "b"], [], ["a", "d"]]
    #start_config = [["a", "b", "c"], [], []]
    #end_config = [["c", "b", "a"], [], []]
    #start_config = [["a", "b", "c"], ["e", "f"], ["h", "i"]]
    #end_config = [["i"], ["e", "a"], ["b", "h", "f", "c"]]
    graph = Graph(start_config, end_config)

    result = astar_search(graph)
    print(result)

    t1 = time()
    print("Execution took " + str(round(1000 * (t1 - t0), 2)) + " ms.")
