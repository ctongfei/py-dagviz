from typing import Hashable, Dict, List
import array
import networkx as nx


def visualize_dag(g: nx.DiGraph, round_angle: bool = False) -> str:
    """
    Creates a text rendering of a directed acyclic graph (DAG) for visualization purposes in a terminal.

    :param g: A directed acyclic graph, of type `nx.DiGraph`
    :param round_angle: Whether to use a round-angled box drawing character or not
    :return: A multi-line string representation of the directed acyclic graph, each line corresponding to a node
    """
    assert nx.is_directed_acyclic_graph(g), "Graph contains cycles"

    rows: List[Hashable] = []
    node_to_row: Dict[Hashable, int] = {}
    indents: List[int] = []

    def _process_dag(g: nx.DiGraph, indent: int):
        for sg in nx.weakly_connected_components(g):
            _process_component(g.subgraph(sg), indent=indent)

    def _process_component(g: nx.DiGraph, indent: int):
        sources = [v for v in g.nodes if g.in_degree(v) == 0]
        for i in range(len(sources)):
            node_to_row[sources[i]] = len(rows)
            rows.append(sources[i])
            indents.append(indent + i)
        _process_dag(
            g.subgraph(set(g.nodes).difference(sources)),
            indent=indent + len(sources)
        )

    _process_dag(g, indent=0)
    a = [
        array.array('u', [u' '] * indents[i] * 2)
        for i in range(len(rows))
    ]
    for i, u in enumerate(rows):
        successors = sorted(g.successors(u), key=lambda v: node_to_row[v])
        if len(successors) == 0:
            continue
        last_successor_row = node_to_row[successors[-1]]
        for j in range(i + 1, last_successor_row):
            a[j][indents[i] * 2] = u'│'
        for v in successors[:-1]:
            j = node_to_row[v]
            a[j][indents[i] * 2] = u'┼' \
                if indents[i] > 0 and a[j][indents[i] * 2 - 1] == u'─' \
                else u'├'
            for k in range(indents[i] * 2 + 1, indents[j] * 2):
                a[j][k] = u'─'
        a[last_successor_row][indents[i] * 2] = u'┴' \
            if a[last_successor_row][indents[i] * 2 - 1] == u'─' \
            else (u'╰' if round_angle else u'└')
        for k in range(indents[i] * 2 + 1, indents[last_successor_row] * 2):
            a[last_successor_row][k] = u'─'

    lines: List[str] = [l.tounicode() + "• " + str(i).replace('\n', ' ') for l, i in zip(a, rows)]
    return '\n'.join(lines)
