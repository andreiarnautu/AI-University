##
 #  Worg
 ##
import sys
import copy


class NodeInGraph:
    """  Class containing the info about a node in the search tree """

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent


    def get_path(self):
        """ Function that returns the path from the original state to the current one """
        node_list = []
        node = self
        while node is not None:
            node_list.append(node)
            node = node.parent
        return node_list.reverse()


    def __repr__(self):
        """ Format the node data into something readable """
        return self.state




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
                aux_node = NodeInGraph(info_copy, node)
                element = aux_node.state[i].pop(0)

                for j in range(self.size):
                    if i != j:
                        state_new = copy.deepcopy(aux_node.state)







start_config = [["a"], ["b", "c"], ["d"]]
end_config = [["c", "b"], [], ["a", "d"]]
