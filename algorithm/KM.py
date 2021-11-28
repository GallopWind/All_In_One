# %%
import random
import math
import copy

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
                    if dis < 0.5:
                        l.reachable.add(r)
                        self.table[(l.id, r.id)] = 1.0 / (dis + 0.11)

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
        self.l = set(left_nodes)
        self.r = set(right_nodes)

    def ClearConnect(self):
        for node in self.l:
            node.connect = None
        for node in self.r:
            node.connect = None

    # to fix
    def GetFromWightBipartiteGraph(self, weight_graph):
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
        self.Hungarian_algorithm = Hungarian()

    def Match(self, weight_graph):
        matched_nodes = []
        def UpdateLabel(node):
            has_bigher_than_zero = False
            node.weight_label -= 0.1
            for node in matched_nodes:
                node.weight_label -= 0.1
                node.connect.weight_label += 0.1
                if node.weight_label >0:
                    has_bigher_than_zero = True
            pass

        # init labels
        for node in weight_graph.l:
            max_weight = 0
            for reachable_node in node.reachable:
                weight = weight_graph.weight_table.GetWeight(
                    (node.id, reachable_node.id)
                )
                if weight > max_weight:
                    max_weight = weight
            node.weight_label = max_weight
        for node in weight_graph.r:
            node.weight_label = 0
        # traverse nodes
        for node in weight_graph.l:
            while 1:
                noweight_graph = BipartiteGraph(None, None)
                noweight_graph.GetFromWightBipartiteGraph(weight_graph)
                if Hungarian.DFS_Iteration(noweight_graph, [node]):
                    # take down 
                else:
                    


# %%
# test
left_nodes = set()
right_nodes = set()
l1 = Node(0, "l", 0, 0)
l2 = Node(1, "l", 0, 0)
l3 = Node(2, "l", 0, 0)
r1 = Node(3, "r", 0, 0)
r2 = Node(4, "r", 0, 0)
r3 = Node(5, "r", 0, 0)
l1.reachable.add(r1)
l1.reachable.add(r2)
l1.reachable.add(r3)
l2.reachable.add(r1)
l2.reachable.add(r2)
l3.reachable.add(r1)
left_nodes.add(l1)
left_nodes.add(l2)
left_nodes.add(l3)
right_nodes.add(r1)
right_nodes.add(r2)
right_nodes.add(r3)


graph = BipartiteGraph(left_nodes, right_nodes)
algorithm = Hungarian()
print(algorithm.Match(graph))
# %%
# for i in range(20):
#     left_nodes.add(Node(i, random.random(), random.random()))
# for i in range(20, 40):
#     right_nodes.add(Node(i, random.random(), random.random()))
