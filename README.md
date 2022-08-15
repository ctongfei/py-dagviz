# py-dagviz [![PyPI version](https://badge.fury.io/py/py-dagviz.svg)](https://badge.fury.io/py/py-dagviz)
This package creates a text rendering of a directed acyclic graph (DAG) for visualization purposes in a terminal.
It contains a single function `visualize_dag` that takes a [`networkx.DiGraph`](https://networkx.org/documentation/stable/reference/classes/digraph.html) object from the [networkx](https://networkx.org/) package.
```
• 0
├─• 1
├─┼─• 2
│ ├─┼─• 3
└─│─┴─• 4
  └─• 5
```

### Usage
```python
import networkx as nx
from dagviz import visualize_dag

g = nx.DiGraph()
# Creates the graph to visualize
# If the graph contains cycles (i.e., not a DAG), visualization fails
g.add_nodes_from([0, 1, 2, 3, 4, 5])
g.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 5), (2, 4), (0, 4), (2, 3)])

print(visualize_dag(g, round_angle=False))
# • 0
# ├─• 1
# ├─┼─• 2
# │ ├─┼─• 3
# └─│─┴─• 4
#   └─• 5

print(visualize_dag(g, round_angle=True))  # display may be bad under some terminal fonts
# • 0
# ├─• 1
# ├─┼─• 2
# │ ├─┼─• 3
# ╰─│─┴─• 4
#   ╰─• 5
```
