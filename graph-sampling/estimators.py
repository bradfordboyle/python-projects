#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt
import random
import scipy.stats

class Estimator(object):
    def __init__(self, sample_budget, num_batches, batch_samples):
        self.sample_budget = sample_budget
        self.num_batches = num_batches
        self.batch_samples = batch_samples
        self._n = 0
        self._mean = 0
        self._variance = 0

    def _observation(self, x):
        self._n += 1
        mean = self._mean + (x - self._mean) / float(self.n)
        variance = self._variance + self._mean ** 2 - (mean) ** 2
        variance += (x ** 2 - self._variance - self._mean ** 2) /float(self._n)
        self._mean = mean
        self._variance = variance

    @property
    def n(self):
        return self._n

    @property
    def mean(self):
        return self._mean

    @property
    def std_dev(self):
        return sqrt(self._n * self._variance / float(self._n - 1))


    def confidence(self, level=0.95):
        return scipy.stats.t.ppf((1 + level) / 2.0, self._n - 1) * self.std_dev / sqrt(self._n)
    pass


class MonteCarlo(Estimator):
    def __init__(self, sample_budget, num_batches, batch_samples):
        super(MonteCarlo, self).__init__(sample_budget, num_batches, batch_samples)

    def sample(self, graph):
        """Sample n vertices uniformly at random and return maximum degree"""
        max_degree_estimate = max(random.choice(graph.vs).degree() for _ in range(self.sample_budget))
        self._observation(max_degree_estimate)


class Greedy(Estimator):
    pass


class Annealing(Estimator):
    pass

