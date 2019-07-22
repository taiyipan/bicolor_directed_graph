class BicolorDirectedGraph:
    class GraphNode:
        def __init__(self, val = None):
            self.val = val
            self.edges = {'red': list(), 'blue': list()}

    def __init__(self):
        self.nodes = dict()

    # populate the graph with set number of nodes
    def populate(self, n: int) -> None:
        for i in range(n):
            node = self.GraphNode(i)
            self.nodes[i] = node

    # add multiple edges of same color
    def multi_add(self, paths: list, color: str) -> None:
        for path in paths:
            self.add(path, color)

    # add 1 edge of 1 color to the graph, create nodes ad hoc if needed
    def add(self, path: list, color: str) -> None:
        assert len(path) == 2, 'Path must be a list of 2 values'
        assert color == 'red' or color == 'blue', 'Color must be either red or blue'
        # locate node1, create it if not found
        node1 = self.find(path[0])
        if node1 is None:
            node1 = self.GraphNode(path[0])
            self.nodes[path[0]] = node1
        # locate node2, create it if not found
        node2 = self.find(path[1])
        if node2 is None:
            node2 = self.GraphNode(path[1])
            self.nodes[path[1]] = node2
        # encode colored edge data
        if color == 'red':
            node1.edges['red'].append(node2)
        elif color == 'blue':
            node1.edges['blue'].append(node2)

    def find(self, val: int) -> GraphNode:
        return self.nodes.get(val)

    def analyze(self) -> list:
        if len(self.nodes) == 0:
            return []
        elif len(self.nodes) == 1:
            return [0]
        paths = len(self.nodes) * [-1] # -1 means not reachable, here as default state
        paths[0] = 0 # 0 node is the starting node, hence always reachable
        for i in range(1, len(paths)):
            paths[i] = self.breadth_first_search(self.nodes[0], self.nodes[i])
        return paths

    # determine if one can go from n1 to n2 in an alternating color pattern
    # if reachable, return number of edges it traverses
    # if not, return -1
    def breadth_first_search(self, n1: GraphNode, n2: GraphNode) -> int:
        # create seen dictionary: keep track of edges that have been seen already
        seen = {'red': list(), 'blue': list()}
        # start with prev_color = red
        pattern1 = self.bfs([n1], n2, seen, 'red', 0)
        # start with prev_color = blue
        pattern2 = self.bfs([n1], n2, seen, 'blue', 0)
        # return shortest path
        if pattern1 == -1 and pattern2 == -1:
            return -1
        elif pattern1 == -1:
            return pattern2
        elif pattern2 == -1:
            return pattern1
        else:
            return min(pattern1, pattern2)

    # a breadth-first recursive and iterative hybrid algorithm with alternating color search patterns
    def bfs(self, layer: list, target: GraphNode, seen: list, prev_color: str, steps: int) -> int:
        # stop condition: if further layer is no longer possible
        # all edges that can be reached have been reached, so further layer is impossible
        if not layer:
            return -1
        # determine next layer
        next_layer = list()
        # option 1: explore blue edges for next layer
        if prev_color == 'red':
            for node in layer:
                for neighbor in node.edges['blue']:
                    if neighbor is target: # if target is located
                        return steps + 1
                    edge = [node.val, neighbor.val]
                    if edge not in seen['blue']: # if edge has not been seen before
                        next_layer.append(neighbor)
                        seen['blue'].append(edge)
            return self.bfs(next_layer, target, seen, 'blue', steps + 1)
        # option 2: explore red edges for next layer
        elif prev_color == 'blue':
            for node in layer:
                for neighbor in node.edges['red']:
                    if neighbor is target: # if target is located
                        return steps + 1
                    edge = [node.val, neighbor.val]
                    if edge not in seen['red']: # if edge has not been seen before
                        next_layer.append(neighbor)
                        seen['red'].append(edge)
            return self.bfs(next_layer, target, seen, 'red', steps + 1)

class Solution: # solution to leetcode problem 5132 
    def shortestAlternatingPaths(self, n: int, red_edges: list, blue_edges: list) -> list:
        graph = BicolorDirectedGraph()
        graph.populate(n)
        graph.multi_add(red_edges, 'red')
        graph.multi_add(blue_edges, 'blue')
        return graph.analyze()
