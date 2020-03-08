##
 #  Worg
 ##
class Graph:
    """ Class representing the graph """

    def __init__(self, graph_dict = None, directed = True):
        self.graph_dict = graph_dict or {}


    def connect(self, a, b, distance = 1):
        """ Add a link from A to B of given distance """
        self.graph_dict.setdefault(a, {})[b] = distance


    def get(self, a, b = None):
        """ Get neighbours or a neighbour """
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)


    def nodes(self):
        """ Return a list of nodes in the graph """
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)



class Node:
    """ Class representing a node """

    def __init__(self, name : str, parent : str):
        self.name = name
        self.parent = parent
        self.g = 0  #  Distance to start node
        self.h = 0  #  Distance to goal node
        self.f = 0  #  Total cost


    def __eq__(self, other):
        return self.name == other.name


    def __lt__(self, other):
        """ Comparator used when sorting """
        return self.f < other.f


    def __repr__(self):
        return ('({0}, {1})'.format(self.position, self.f))



def astar_search(graph, heuristics, start_id, end_id):
    #  Create lists for open nodes and closed nodes
    open_nodes = []
    closed_nodes = []

    #  Create the start and end nodes
    start_node = Node(start_id, None)
    end_node = Node(end_id, None)

    open_nodes.append(start_node)
    while len(open_nodes) > 0:
        open_nodes.sort()
        current_node = open_nodes.pop(0)
        closed_nodes.append(current_node)

        #  Check if we reached the goal and return the path
        if current_node == end_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name + ": " + str(current_node.g))
                current_node = current_node.parent

            path.append(start_node.name + ": " + str(start_node.g))
            return path[::-1]

        #  Get neighbours
        neighbours = graph.get(current_node.name)
        for key, value in neighbours.items():
            neighbour = Node(key, current_node)
            if neighbour in closed_nodes:
                continue
            # Calculate full path cost
            neighbour.g = current_node.g + graph.get(current_node.name, neighbour.name)
            neighbour.h = heuristics.get(neighbour.name)
            neighbour.f = neighbour.g + neighbour.h


            #  Check if the neighbour is in open list and if it has a lower f value
            worth_adding = True
            for node in open_nodes:
                if neighbour == node and neighbour.f > node.f:
                    worth_adding = False
                    continue

            if worth_adding:
                open_nodes.append(neighbour)
    return None


def main():
    graph = Graph()

    #  Hardcode the input
    graph.connect('a', 'b', 3)
    graph.connect('a', 'c', 9)
    graph.connect('a', 'd', 7)
    graph.connect('b', 'f', 100)
    graph.connect('b', 'e', 4)
    graph.connect('c', 'e', 10)
    graph.connect('c', 'g', 6)
    graph.connect('d', 'i', 4)
    graph.connect('e', 'c', 1)
    graph.connect('e', 'f', 8)
    graph.connect('g', 'e', 7)
    graph.connect('i', 'j', 2)

    heuristics = {}
    heuristics['a'] = 0
    heuristics['b'] = 10
    heuristics['c'] = 3
    heuristics['d'] = 7
    heuristics['e'] = 8
    heuristics['f'] = 0
    heuristics['g'] = 14
    heuristics['i'] = 3
    heuristics['j'] = 1
    heuristics['k'] = 2

    path = astar_search(graph, heuristics, 'a', 'f')
    print(path)


if __name__ == '__main__':
    main()
