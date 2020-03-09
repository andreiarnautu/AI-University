##
 #  Worg
 ##
import sys
import copy
from queue import PriorityQueue

class NodeInGraph:
    """  Class containing the info about a node in the search tree """

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.g = 0  #  Distance to start node
        self.h = 0  #  Distance to end node
        self.f = 0  #  Total distance


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
        stack_id = {}
        for i in range(len(self.state)):
            for element in self.state[i]:
                stack_id[element] = i

        heuristic_cost = 0
        for i in range(len(end_node.state)):
            for element in end_node.state[i]:
                heuristic_cost += abs(i - stack_id[element])
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


        for stack_string in stack_list[::-1]:
            string += stack_string
        string += "\n"
        return string


    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.f < other.f


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
    open_nodes = []
    closed_nodes = []

    #  Create the start and end node
    start_node = NodeInGraph(graph.start_config, None)
    end_node = NodeInGraph(graph.end_config, None)
    open_nodes.append(start_node)

    while len(open_nodes) > 0:
        open_nodes.sort()
        current_node = open_nodes.pop(0)

        if current_node in closed_nodes:
            continue

        closed_nodes.append(current_node)

        #  Check if we reached the goal and return the path
        if current_node == end_node:
            return current_node.get_path()


        #  Get neighbours
        neighbours = graph.expand(current_node)
        for next_node in neighbours:
            if next_node in closed_nodes:
                continue
            #  Calculate full path cost
            next_node.g = current_node.g + 1
            next_node.h = next_node.compute_heuristic(end_node)
            next_node.f = next_node.g + next_node.h

            #  Check if the neighbour is in open list and if it has a lower f value
            worth_adding = True
            for node in open_nodes:
                if next_node == node and next_node.f > node.f:
                    wort_adding = False
                    break

            if worth_adding:
                open_nodes.append(next_node)

    return None


start_config = [["a"], ["b", "c"], ["d"]]
end_config = [["c", "b"], [], ["a", "d"]]
graph = Graph(start_config, end_config)

result = astar_search(graph)
print(result)
