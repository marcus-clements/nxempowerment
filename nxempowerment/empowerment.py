import logging

from typing import Tuple

import networkx as nx

from nxempowerment.utils import logzero


logger = logging.getLogger(__name__)


def succ(graph: nx.Graph, node: tuple, seen: set, step: int, max_steps: int) -> None:
    step += 1
    for n in nx.neighbors(graph, node):
        seen.add(n)
        if step < max_steps:
            succ(graph, n, seen, step, max_steps)


def node_empowerment(graph: nx.Graph, node: tuple, num_steps: int) -> Tuple[set, float]:
    # Include the start node so it is not visited by the recursion
    successors = {node}
    succ(graph, node, successors, 0, num_steps)
    # Do not include the start node to compute the empowerment
    return logzero(max(len(successors) - 1, 0))


def graph_node_empowerment(graph: nx.Graph, num_steps: int) -> dict:
    logger.info("Computing Empowerment for a graph of %s", graph.number_of_nodes())
    empowerment = {}
    for node in nx.nodes(graph):
        empowerment[node] = node_empowerment(graph, node, num_steps)
    logger.info("Finished Computing Empowerment for a graph of %s", graph.number_of_nodes())
    return empowerment
