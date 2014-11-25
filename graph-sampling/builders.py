#!/usr/bin/env python
# -*- coding: utf-8 -*-

import igraph as _ig

def ErdosRenyi(n, p):
    def f():
        return _ig.Graph.Erdos_Renyi(n=n, p=p)
    return f


def Barabasi(n, m):
    def f():
        return _ig.Graph.Barabasi(n=n, m=m)
    return f


def Canon(filename):
    graph = _ig.Graph.Read_GraphMLz(filename)
    def f():
        return graph
    return f
