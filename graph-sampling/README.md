graph-sampling
==============

Implementation of several different methods for estimating a graphs max degree
by only visiting a faction of the nodes. Different estimators are implemented
as subclasses of a base estimator class that provides iterative updates of
sample mean, sample variance, and confidence interval. Experiments are defined
via:
    1. the type of random graph to generate
    2. the number of random graphs to generate
    3. where to save the results
    4. what type of estimators to use
    5. the different sampling budgets to use
Random graphs are provided through builder functions that accept the size of
the graph and returns a function for generating the random samples.

