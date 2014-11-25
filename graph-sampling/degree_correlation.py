#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import builders as _b

def degree_correlation(G):
    n = max(G.degree())
    dc = [[0 for i in range(n)] for j in range(n)]
    for e in G.es:
        s,t = G.vs[e.tuple].degree()
        s -= 1
        t -= 1
        dc[s][t] += 1
        dc[t][s] += 1
    return dc


def write_degree_correlation(dc, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        for values in dc:
            writer.writerow(values)


if __name__ == '__main__':
    import sys

    #G = _b.ErdosRenyi(10000, 5./10000)()
    #G = _b.Barabasi(10000, 2)()
    G = _b.Canon(sys.argv[2])()
    dc = degree_correlation(G)
    write_degree_correlation(dc, sys.argv[1])
