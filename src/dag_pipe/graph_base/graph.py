"""
each node represents a graph_base:
edge

function -> graph_base
graph_base -> computational graph_base

support batch?

"""

import networkx as nx


class AbstractDAG(object):
    def __init__(self):
        self.graph = nx.DiGraph()

    def _add_edges_from(self, *args):
        for arg_tuple in args:
            _from, _to = arg_tuple
            self.graph.add_edge(_from, _to)

    def add_edge(self, _from, _to):
        self.graph.add_edge(_from, _to)

    def _is_directed_acyclic_graph(self):
        return nx.is_directed_acyclic_graph(self.graph)

    @property
    def is_directed_acyclic_graph(self):
        return self._is_directed_acyclic_graph()


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


