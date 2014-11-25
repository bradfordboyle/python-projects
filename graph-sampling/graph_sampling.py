#!/usr/bin/env python
# -*- coding: utf-8 -*-

import builders as _b
import random
import progressbar as _p
import math
import Estimator as _e


def annealing(graph, n):
    estimate = 0
    cool = 1e-5 ** (1. / n)
    temperature = 10000

    v = random.choice(graph.vs)
    estimate = max(estimate, v.degree())
    while temperature > 0.1:
        temperature *= cool
        estimate = max(estimate, v.degree())
        v = annealing_next_vertex(v, temperature)
    return estimate


def annealing_next_vertex(v, temperature):
    d = v.degree()
    if d == 0:
        return random.choice(v.graph.vs)
    else:
        v_prime = random.choice(v.neighbors())
        d_prime = v_prime.degree()
        p = math.exp(min(0, d_prime - d) / temperature)
        U = random.random()
        if d_prime >= d or U <= p:
            return v_prime
        else:
            return v


def monte_carlo(graph, n):
    """Sample n vertices uniformly at random and return maximum degree"""
    return max(random.choice(graph.vs).degree() for _ in range(n))


def greedy(graph, n):
    """Greedy walk maximum degree estimator.

    Select a random vertex, look at the degrees of all adjacent vertices, select
    (if possible) a new neighbor that has maximum degree among all neighbors,
    move to that vertex, and repeat at most n times.
    """
    estimate = 0

    v = random.choice(graph.vs)
    if v.degree() == 0:
        return estimate

    for i in range(n):
        estimate = max(estimate, v.degree())
        v = next_vertex(v)
        if v is None:
            break

    return estimate


def greedy_restart(graph, n):
    """Greedy walk maximum degree estimator.

    Select a random vertex, look at the degrees of all adjacent vertices, select
    (if possible) a new neighbor that has maximum degree among all neighbors,
    move to that vertex, and repeat at most n times.
    """
    v = random.choice(graph.vs)
    estimate = v.degree()
    n -= 1
    while n > 0:
        if len(v.neighbors()) == 0:
            v = random.choice(graph.vs)
        else:
            v = next_vertex(v)
            if v is None:
                v = random.choice(graph.vs)
        estimate = max(estimate, v.degree())
        n -= 1
    return estimate


def scheme_three(graph, k, m):
    """Hybrid greedy walk maximum degree estimator.

    Arguments:
        k -- number of independent samples
        m -- maximum length of walk from any vertex
    """
    estimate = 0

    for i in range(k):
        v = random.choice(graph.vs)
        if len(v.neighbors()) == 0:
            continue
        for j in range(m):
            estimate = max(estimate, v.degree())
            v = next_vertex(v)

    return estimate


def scheme_four(G, k, m):
    """Simplified hybrid greedy walk maximum degree estimator.

    The difference between this estimator and the one above is that the next
    neighbor is chosen uniformly at random.
    """
    Z = 0

    for i in range(k):
        v = random.choice(G.vs)
        if len(v.neighbors()) == 0:
            continue
        for j in range(m):
            Z = max(Z, v.degree())
            v = random.choice(v.neighbors())

    return Z

def next_vertex(v):
    """Returns next vertex on greedy walk.
    """
    v_prime = max(v.neighbors(), key=lambda v: v.degree())
    if v_prime.degree() < v.degree():
        return None
    return v_prime


def relative_error(value, estimate):
    if value < estimate:
        raise Exception
    return 1 - float(estimate)/float(value)


def experiment(graph_maker, sample_sizes, num_trials, results):
    widgets = ['Completed: ', _p.Percentage(), ' ', _p.Bar(), _p.ETA()]
    for sample in sample_sizes:
        monte_carlo_est = _e.Estimator()
        greedy_est = _e.Estimator()
        greedy_restart_est = _e.Estimator()
        annealing_est = _e.Estimator()
        progress = _p.ProgressBar(widgets=widgets, maxval=num_trials)
        progress.start()
        for trial in range(num_trials):
            graph = graph_maker()
            max_degree = max(graph.degree())
            monte_carlo_est.observation(relative_error(max_degree, monte_carlo(graph, sample)))
            greedy_est.observation(relative_error(max_degree, greedy(graph, sample)))
            greedy_restart_est.observation(relative_error(max_degree, greedy_restart(graph, sample)))
            annealing_est.observation(relative_error(max_degree, annealing(graph, sample)))

            progress.update(trial + 1)

        progress.finish()
        data = '{:.4f}'.format(float(sample) / len(graph.vs))
        data += '\t{:.4f}\t{:.4f}'.format(monte_carlo_est.mean, monte_carlo_est.confidence())
        data += '\t{:.4f}\t{:.4f}'.format(greedy_est.mean, greedy_est.confidence())
        data += '\t{:.4f}\t{:.4f}'.format(greedy_restart_est.mean, greedy_restart_est.confidence())
        data += '\t{:.4f}\t{:.4f}'.format(annealing_est.mean, annealing_est.confidence())
        data += '\n'
        results.write(data)


if __name__ == '__main__':
    import sys
    num_vertices = int(sys.argv[1])
    num_trials = int(sys.argv[2])
    results = open(sys.argv[3], 'w')
    graph_maker = _b.ErdosRenyi(num_vertices, 5.0/num_vertices)
    #graph_maker = _b.Barabasi(num_vertices, 2)
    #graph_maker = _b.Canon(sys.argv[4])
    sample_sizes = [int(0.01 * (i+1) * num_vertices) for i in range(10)]
    experiment(graph_maker, sample_sizes, num_trials, results)
