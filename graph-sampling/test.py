#!/usr/bin/env python
# -*- coding: utf-8 -*-

from builders import ErdosRenyi, Barabasi
from Experiment import Experiment
from Estimator import MonteCarlo, Greedy, GreedyRestart, Annealing

config = {
    'graph_maker': ErdosRenyi(n=100, p=5.0/100),
    'num_trials': 10000,
    'filename': 'results/Erdos-Renyi-1e2.tsv',
    'estimator_types': [MonteCarlo, Greedy, GreedyRestart, Annealing],
    'budgets': [i + 1 for i in range(10)]
}
e = Experiment(**config)
e.run()

config = {
    'graph_maker': ErdosRenyi(n=1000, p=5.0/1000),
    'num_trials': 10000,
    'filename': 'results/Erdos-Renyi-1e3.tsv',
    'estimator_types': [MonteCarlo, Greedy, GreedyRestart, Annealing],
    'budgets': [10 * (i + 1) for i in range(10)]
}
e = Experiment(**config)
e.run()

config = {
    'graph_maker': ErdosRenyi(n=10000, p=5.0/10000),
    'num_trials': 10000,
    'filename': 'results/Erdos-Renyi-1e4.tsv',
    'estimator_types': [MonteCarlo, Greedy, GreedyRestart, Annealing],
    'budgets': [100 * (i + 1) for i in range(10)]
}
e = Experiment(**config)
e.run()

config = {
    'graph_maker': ErdosRenyi(n=100000, p=5.0/100000),
    'num_trials': 10000,
    'filename': 'results/Erdos-Renyi-1e5.tsv',
    'estimator_types': [MonteCarlo, Greedy, GreedyRestart, Annealing],
    'budgets': [1000 * (i + 1) for i in range(10)]
}
e = Experiment(**config)
e.run()

config = {
    'graph_maker': Barabasi(n=100, m=2),
    'num_trials': 10000,
    'filename': 'results/Barabasi-1e2.tsv',
    'estimator_types': [MonteCarlo, Greedy, GreedyRestart, Annealing],
    'budgets': [i + 1 for i in range(10)]
}
e = Experiment(**config)
e.run()

config = {
    'graph_maker': Barabasi(n=1000, m=2),
    'num_trials': 10000,
    'filename': 'results/Barabasi-1e3.tsv',
    'estimator_types': [MonteCarlo, Greedy, GreedyRestart, Annealing],
    'budgets': [10 * (i + 1) for i in range(10)]
}
e = Experiment(**config)
e.run()

config = {
    'graph_maker': Barabasi(n=10000, m=2),
    'num_trials': 10000,
    'filename': 'results/Barabasi-1e4.tsv',
    'estimator_types': [MonteCarlo, Greedy, GreedyRestart, Annealing],
    'budgets': [100 * (i + 1) for i in range(10)]
}
e = Experiment(**config)
e.run()

config = {
    'graph_maker': Barabasi(n=100000, m=2),
    'num_trials': 10000,
    'filename': 'results/Barabasi-1e5.tsv',
    'estimator_types': [MonteCarlo, Greedy, GreedyRestart, Annealing],
    'budgets': [1000 * (i + 1) for i in range(10)]
}
e = Experiment(**config)
e.run()
