# %%
import random
import math
import copy

# %%
class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.connect = None
        self.reachable = set()  # only for right nodes.
        self.weight_label = -1


class WeightBipartiteGraph:
    class WeightTable:
        def __init__(self):
            self.table = {}

        def ComputeWeight(self, graph):
            for l in graph.l:
                for r in graph.r:
                    dis = math.hypot(l.x - r.x, l.y - r.y)
                    if dis < 0.5:
                        l.reachable.add(r)
                        self.table[(l.id, r.id)] = 1.0 / (dis + 0.11)

        def GetWeight(self, l, r):
            if (l.id, r.id) in self.table.keys():
                return self.table[(l.id, r.id)]

    def __init__(self, left_nodes, right_nodes):
        self.l = left_nodes
        self.r = right_nodes
        self.weight_table = WeightBipartiteGraph.WeightTable()
        self.weight_table.ComputeWeight(self)


class BipartiteGraph:
    def __init__(self, weight_graph):
        self.l = copy.deepcopy(weight_graph.l)
        self.r = copy.deepcopy(weight_graph.r)
        for left_node in self.l:
            for reachable_node in left_node.reachable:
                if (
                    left_node.weight_label + reachable_node.weight_label
                    < weight_graph.weight_table.GetWeight(left_node, reachable_node)
                ):
                    left_node.reachable.remove(reachable_node)


# %%
class Hungarian:
    def __init__(self):
        pass

    def Match(self, weight_graph):
        pass


class KM:
    def __init__(self):
        pass

    def Match(self, graph):
        pass


# %%
left_nodes = set()
right_nodes = set()
for i in range(20):
    left_nodes.add(Node(i, random.random(), random.random()))
for i in range(20, 40):
    right_nodes.add(Node(i, random.random(), random.random()))
