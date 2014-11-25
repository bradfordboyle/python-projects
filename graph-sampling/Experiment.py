#!/usr/bin/env python
# -*- coding: utf-8 -*-
import progressbar as _p

class Experiment(object):
    def __init__(self, graph_maker, **kwargs):
        self.graph_maker = graph_maker
        prop_defaults = {
            'estimator_types': [],
            'budgets': [],
            'widgets': ['Completed: ', _p.Percentage(), ' ', _p.Bar(), _p.ETA()],
            'num_trials': 100,
            'filename': 'results.tsv',
        }

        for (prop, default) in prop_defaults.iteritems():
            setattr(self, prop, kwargs.get(prop, default))
        self.results = open(self.filename, 'w', 0)

    def run(self):
        print('Running experiment...')
        for budget in self.budgets:
            progress = _p.ProgressBar(widgets=self.widgets, maxval=self.num_trials)
            progress.start()

            # re-initialize estimators
            estimators = []
            for est_type in self.estimator_types:
                estimators.append(est_type())

            for trial in range(self.num_trials):
                graph = self.graph_maker()
                for est in estimators:
                    est.observation(graph, budget)
                progress.update(trial + 1)
            progress.finish()

            data = '{:.4f}'.format(budget)
            data += '\t'.join(map(str,estimators))
            data += '\n'
            self.results.write(data)

