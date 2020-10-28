"""
Terms & Defnition:
    node:
    edge:

"""

import networkx as nx
from networkx.algorithms import dag


class WrappedGraphBase(object):
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node):
        self.graph.add_node(node)

    def add_nodes_from(self, nodes):
        self.graph.add_nodes_from(nodes)

    def remove_node(self, node):
        self.graph.remove_node(node)

    def remove_nodes_from(self, nodes):
        self.graph.remove_nodes_from(nodes)

    def nodes(self):
        nodes = set(self.graph.nodes())
        return nodes

    def has_node(self, node):
        if_node_exist = self.graph.has_node(node)
        return if_node_exist

    def add_edge(self, from_, to_):
        self.graph.add_edge(from_, to_)

    def add_edges_from(self, edge_tuples):
        self.graph.add_edges_from(edge_tuples)

    def remove_edge(self, from_, to_):
        self.graph.remove_edge(from_, to_)

    def remove_edges_from(self, edge_tuples):
        self.graph.remove_edges_from(edge_tuples)

    def edges(self):
        edges = set(self.graph.edges)
        return edges

    def edge_exists(self, from_, to_):
        if_edge_exists = self.graph.has_edge(from_, to_)
        return if_edge_exists

    def predecessors(self, node):
        predecessor_set = set(self.graph.predecessors(node))
        return predecessor_set

    def is_a_predecessor_of(self, node, predecessor):
        if_predecessor = self.graph.has_predecessor(node, predecessor)
        return if_predecessor

    def ancestors(self, node):
        ancestor_set = dag.ancestors(self.graph, node)
        return ancestor_set

    def is_an_ancestor_of(self, node, ancestor):
        if_ancestor = (ancestor in self.ancestors(node))
        return if_ancestor

    def successors(self, node):
        successor_set = set(self.graph.successors(node))
        return successor_set

    def is_a_successor_of(self, node, successor):
        if_successor = (successor in self.successors(node))
        return if_successor

    def descendants(self, node):
        descendant_set = dag.descendants(self.graph, node)
        return descendant_set

    def is_a_descendant_of(self, node, descendant):
        if_descendant = (descendant in self.descendants(node))
        return if_descendant

    def is_directed_acyclic_graph(self):
        return nx.is_directed_acyclic_graph(self.graph)

    def shortest_path(self, from_, to_):
        return nx.shortest_path(self.graph, from_, to_)

    def _check_node_in_degree(self, node):
        degree = self.graph.in_degree(node)
        return degree

    def _check_node_out_degree(self, node):
        degree = self.graph.out_degree(node)
        return degree

    def is_source(self, node):
        if (self._check_node_in_degree(node) == 0) and (self._check_node_out_degree(node) >= 0):
            is_source = True
        else:
            is_source = False

        return is_source

    def is_source_of(self, source, node):
        is_source = self.is_source(node=source)
        if is_source and (node in self.ancestors(node)):
            is_source_and_connected = True
        else:
            is_source_and_connected = False

        return is_source_and_connected

    def sources(self, node):
        source_set = set()
        for ancestor in self.ancestors(node):
            if self.is_source(ancestor):
                source_set.add(ancestor)
        return source_set

    def all_sources(self):
        source_set = set()
        for node in self.nodes():
            if self.is_source(node):
                source_set.add(node)
        return source_set

    def is_leaf(self, node):
        if (self._check_node_in_degree(node) >= 0) and (self._check_node_out_degree(node) == 0):
            is_leaf = True
        else:
            is_leaf = False

        return is_leaf

    def is_leaf_of(self, leaf, node):
        is_leaf = self.is_leaf(node=leaf)
        if is_leaf and (node in self.descendants(node)):
            is_leaf_and_connected = True
        else:
            is_leaf_and_connected = False

        return is_leaf_and_connected

    def leaves(self, node):
        leaf_set = set()
        for descendant in self.descendants(node):
            if self.is_leaf(descendant):
                leaf_set.add(descendant)
        return leaf_set

    def all_leaves(self):
        leaf_set = set()
        for node in self.nodes():
            if self.is_leaf(node):
                leaf_set.add(node)
        return leaf_set

    def is_isolate(self, node):
        if (self._check_node_in_degree(node) == 0) and (self._check_node_out_degree(node) == 0):
            is_isolate = True
        else:
            is_isolate = False

        return is_isolate

    def all_isolates(self):
        isoloates = nx.isolates(self.graph)
        return isoloates

    def topological_sort(self):
        return nx.topological_sort(self.graph)

    def partition_graph_into_trees(self):
        pass


class ComputeGraph(object):
    def __init__(self):
        pass

    def _import_process(self):
        pass

    def propagate(self):
        pass

    def roots(self):
        pass

    def gen_computational_path(self):
        pass

    def validate_net(self):
        pass

    def find_next_processes(self):
        pass

    def find_dependent_processes(self):
        pass


