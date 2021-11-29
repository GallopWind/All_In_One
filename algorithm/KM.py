# %%
import random
import math
import copy
import matplotlib.pyplot as plt

# %%
class Node:
    def __init__(self, id, bipartite, x, y):
        self.id = id
        self.bipartite = bipartite
        self.x = x
        self.y = y
        self.connect = None
        self.reachable = set()  # only for right nodes.
        self.weight_label = -1

    def __eq__(self, other):
        if other == None:
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class WeightBipartiteGraph:
    class WeightTable:
        def __init__(self):
            self.table = {}

        def ComputeWeight(self, graph):
            for l in graph.l:
                for r in graph.r:
                    dis = math.hypot(l.x - r.x, l.y - r.y)
                    self.table[(l.id, r.id)] = dis

        def GetWeight(self, l, r):
            if (l.id, r.id) in self.table.keys():
                return self.table[(l.id, r.id)]
            else:
                return False

    def __init__(self, left_nodes, right_nodes):
        self.l = left_nodes
        self.r = right_nodes
        self.weight_table = WeightBipartiteGraph.WeightTable()
        self.weight_table.ComputeWeight(self)


class BipartiteGraph:
    def __init__(self, left_nodes, right_nodes):
        self.l = left_nodes
        self.r = right_nodes

    def ClearConnect(self):
        for node in self.l:
            node.connect = None
        for node in self.r:
            node.connect = None

    # to fix
    def GetFromWightBipartiteGraph(self, weight_graph):
        self.l = weight_graph.l
        self.r = weight_graph.r
        for left_node in self.l:
            left_node.reachable = set()
            for right_node in self.r:
                if (
                    left_node.weight_label + right_node.weight_label
                    >= weight_graph.weight_table.GetWeight(left_node, right_node)
                ):
                    left_node.reachable.add(right_node)


# %%
class Hungarian:
    def __init__(self):
        pass

    # DFS
    # recursion
    def DFS_Recursion(graph, route):
        end = route[-1]
        child_branch_node = []
        for node in end.reachable:
            if node not in route:
                if node.connect != None:
                    child_branch_node.append((node, node.connect))
                else:
                    # finish search and we found.
                    route.append(node)
                    return True
        if not child_branch_node:
            # finish search and not found.
            return False
        else:
            # continue search
            for node_pair in child_branch_node:
                copy_route = copy.copy(route)
                copy_route.extend(node_pair)
                if Hungarian.DFS_Recursion(graph, copy_route):
                    route.extend(copy_route[len(route) :])
                    return True
            # not found
            return False

    # iteration
    def DFS_Iteration(graph, route):
        stack = [route]
        Trash = []
        while 1:
            if not stack:
                return False
            tmp_route = stack.pop()
            end = tmp_route[-1]
            for node in end.reachable:
                if node not in tmp_route:
                    if node.connect != None:
                        new_route = copy.copy(tmp_route)
                        new_route.extend((node, node.connect))
                        stack.append(new_route)
                    else:
                        tmp_route.append(node)
                        # write tmp_route into route
                        route.extend(tmp_route[len(route) :])
                        return True

    def Match(self, graph):

        for node in graph.l:
            route = [node]
            if Hungarian.DFS_Iteration(graph, route):
                i = 0
                while i < len(route):
                    route[i].connect = route[i + 1]
                    route[i + 1].connect = route[i]
                    i += 2
            else:
                return False
        return True


# %%
class KM:
    def __init__(self):
        pass

    def Match(self, weight_graph):
        matched_nodes = []

        def UpdateLabel(to_match_node):
            to_match_node.weight_label += 0.1
            for matched_node in matched_nodes:
                matched_node.weight_label += 0.1
                matched_node.connect.weight_label -= 0.1

        # init labels
        for node in weight_graph.l:
            min_weight = 2
            for reachable_node in node.reachable:
                weight = weight_graph.weight_table.GetWeight(
                    (node.id, reachable_node.id)
                )
                if weight < min_weight:
                    min_weight = weight
            node.weight_label = min_weight
        for node in weight_graph.r:
            node.weight_label = 0
        # traverse nodes
        for node in weight_graph.l:
            while 1:
                noweight_graph = BipartiteGraph(None, None)
                noweight_graph.GetFromWightBipartiteGraph(weight_graph)
                route = [node]
                if Hungarian.DFS_Iteration(noweight_graph, route):
                    # take down
                    matched_nodes.append(node)
                    i = 0
                    while i < len(route):
                        route[i].connect = route[i + 1]
                        route[i + 1].connect = route[i]
                        i += 2
                    break
                else:
                    UpdateLabel(node)
        return True


# %%
# test
left_nodes = set()
right_nodes = set()
for i in range(10):
    left_nodes.add(
        Node(i, "l", random.random() * 0.2 + i * 0.1, random.random() * 0.2 + i * 0.1)
    )
for i in range(10, 20):
    right_nodes.add(
        Node(
            i,
            "r",
            random.random() * 0.2 + (i - 10) * 0.1,
            random.random() * 0.2 + (i - 10) * 0.1,
        )
    )

graph = WeightBipartiteGraph(left_nodes, right_nodes)
algorithm = KM()
print(algorithm.Match(graph))
# %%
# visualize
figure = plt.figure()
ax = figure.add_subplot(1, 1, 1)
for node in left_nodes:
    ax.plot((node.x, node.connect.x), (node.y, node.connect.y))
figure.show()

# %%
