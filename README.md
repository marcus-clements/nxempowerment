# Compute Empowerment for nodes of a graph #

This package provides functions to compute _Empowerment_ for nodes of a _NetworkX_ graph.

The code was developed to be able to compute empowerment for Street Networks using OSMNX which is based on the NetworkX library. For the original research thesis:
[Empowerment and Relevant Goal Information as Alternatives to Graph-Theoretic Centrality for Navigational Decision Making](https://uhra.herts.ac.uk/handle/2299/22616)

For information about Empowerment see:

[Empowerment Wikipedia page](https://en.wikipedia.org/wiki/Empowerment_(artificial_intelligence))

[Empowerment An Introduction (Salge et al. 2014)](https://link.springer.com/chapter/10.1007%2F978-3-642-53734-9_4)

## Graph worlds ##

The nodes (vertices) of the graph represent states in a discrete world in which an agent operates with a deterministic transition function i.e. p(s|a) = {0,1} 

The agent has five actions available {N,S,W,E,o} where o is do nothing - wait for 1 time step.
The edges of the graph represent the transition function, if a 'N' edge exists from node 3 to node 4 then p(S=4 | S=3, A=N) = 1. Conversely if the 'N' edge does not exist from node 3 to node 4 then p(S=4 | S=3, A=N) = 0.

Note that the graphs are Directed Graphs

## Getting Started ##
For easiest set up create a virtual environment based on Python 3.8.8
There are lots of ways of doing this but I like pyenv virtualenv

`pyenv install 3.8.8`

`pyenv virtualenv 3.8.8 nxempowerment`

`pyenv local nxempowerment`

Install the dependencies:

`pip install -r requirements.txt`

If you want to run the tests:

`pip install -r requirements.txt`

Copy .env.example and edit the values to suit your environment.


## USAGE ##

1. Create an empty DiGraph in Network X 
2. Assign the set of possible actions as a graph attribute
3. Add nodes and edges. The edges must be labeled with an action.
4. Call `nxempowerment.empowerment.graph_node_empowerment(graph, n_steps)` where n_steps is the number of steps of the "empowerment horizon" to compute - this returns a dictionary of nodes and empowerment values.
5. Assign the dictiononary to the graph using `networkx.set_attribute_values()`
6. Plot a visualisation of the graph with `utils.plot_graph_with_measure()`


See `scripts/test_grid_worlds.py` for an example.

To plot a couple of example graphs with empowerment:

`PYTHONPATH=. python scripts/plot_grid_worlds.py`

## TESTS ##

In the root of the repo

`PYTHONPATH=. pytest .`

For PyCharm set the test runner to `pytest`
