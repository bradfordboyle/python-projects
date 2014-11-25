!/usr/bin/env python
# -*- coding: utf-8 -*-
import igraph

def gradient_graph(graph):
    g_graph = igraph.Graph(directed=True)
    g_graph.add_vertices(len(graph.vs))

    for v in graph.vs:
        if len(v.neighbors()) == 0:
            continue
        max_degree_neighbor = max(v.neighbors(), key=lambda v: v.degree())
        if max_degree_neighbor.degree() > v.degree():
            g_graph.add_edge(v.index, max_degree_neighbor.index)

    return g_graph


def save_graph(graph):
    g_graph = gradient_graph(graph)
    layout = graph.layout('fr')
    igraph.plot(graph, 'graph.pdf', layout=layout)
    igraph.plot(g_graph, 'gradient_graph.pdf', layout=layout)


if __name__ == '__main__':
    #graph = igraph.Graph.Erdos_Renyi(n=100, p=5.0/100.)
    #graph = igraph.Graph.Barabasi(n=100, m=2)
    graph = igraph.Graph.Read_GraphMLz('canon-dslr-user-group.graphml.gz')
    save_graph(graph)