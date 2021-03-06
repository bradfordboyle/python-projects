#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt, exp
import random
import scipy.stats


class Estimator(object):
    def __init__(self):
        self._n = 0
        self._M = 0
        self._S = 0

    def __str__(self):
        return '\t{:.4f}\t{:.4f}'.format(self._mean, self.confidence())

    def _observation(self, x):
        delta = x - self._M
        self._M += delta / float(self.n + 1)
        self._S += delta * (x - self._M)
        self._n += 1

    @property
    def n(self):
        return self._n

    @property
    def mean(self):
        return self._M

    @property
    def variance(self):
        return self._S / float(self._n - 1)

    def confidence(self, level=0.95):
        t = scipy.stats.t.ppf((1 + level) / 2.0, self._n - 1)
        return t * sqrt(self.variance / self._n)


class MonteCarlo(Estimator):
    def observation(self, graph, budget):
        """Sample sample_budget vertices uniformly at random and return maximum degree"""
        max_degree = max(graph.degree())
        estimate = max(random.choice(graph.vs).degree() for _ in range(budget))
        relative_error = float(max_degree - estimate) / float(max_degree)
        self._observation(relative_error)


class Greedy(Estimator):
    def observation(self, graph, budget):
        """Greedy walk maximum degree estimator.

        Select a random vertex, look at the degrees of all adjacent vertices, select (if possible) a new neighbor that
        has maximum degree among all neighbors, move to that vertex, and repeat at most n times.
        """
        max_degree = max(graph.degree())
        estimate = 0
        v = random.choice(graph.vs)
        for i in range(budget):
            estimate = max(estimate, v.degree())
            try:
                v_prime = max(v.neighbors(), key=lambda v: v.degree())
            except ValueError:
                break
            if v_prime.degree() < v.degree():
                break
            v = v_prime

        relative_error = float(max_degree - estimate) / float(max_degree)
        self._observation(relative_error)


class GreedyRestart(Estimator):
    def observation(self, graph, budget):
        """Greedy walk maximum degree estimator.

        Select a random vertex, look at the degrees of all adjacent vertices, select
        (if possible) a new neighbor that has maximum degree among all neighbors,
        move to that vertex, and repeat at most n times.
        """
        max_degree = max(graph.degree())
        estimate = 0
        v = random.choice(graph.vs)
        for i in range(budget):
            estimate = max(estimate, v.degree())
            try:
                v_prime = max(v.neighbors(), key=lambda v: v.degree())
            except ValueError:
                v_prime = random.choice(graph.vs)
            if v_prime.degree() < v.degree():
                v_prime = random.choice(graph.vs)
            v = v_prime

        relative_error = float(max_degree - estimate) / float(max_degree)
        self._observation(relative_error)

class Annealing(Estimator):
    def observation(self, graph, budget):
        max_degree = max(graph.degree())
        estimate = 0
        cool = 1e-5 ** (1. / budget)
        temperature = 10000
        v = random.choice(graph.vs)
        while temperature > 0.1:
            temperature *= cool
            d = v.degree()
            estimate = max(estimate, d)
            # select next vertex
            try:
                v_prime = random.choice(v.neighbors())
            except IndexError:
                v_prime = random.choice(graph.vs)
            d_prime = v_prime.degree()
            p = exp(min(0, d_prime - d) / temperature)
            uniform_rv = random.random()
            if d_prime >= d or uniform_rv <= p:
                v = v_prime

        relative_error = float(max_degree - estimate) / float(max_degree)
        self._observation(relative_error)
