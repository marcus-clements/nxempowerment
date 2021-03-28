import math
from random import randint
from typing import List

import networkx as nx


class GridWorldGraph:
    def __init__(self, randomise_actions: bool = False, euclidean_dist: bool = True):
        self.randomise_actions = randomise_actions
        self.euclidean_dist = euclidean_dist

    _map = None

    def graph(self) -> nx.Graph:
        return generate_grid_world(self._map, False, self.randomise_actions)

    def graph_diag(self) -> nx.Graph:
        return generate_grid_world(self._map, True, self.randomise_actions, self.euclidean_dist)


class GridWorldGraph2Rooms(GridWorldGraph):
    def graph(self, width: int=9, height: int=5):
        graph = nx.empty_graph(create_using=nx.DiGraph())
        graph.graph['actions'] = {'N', 'S', 'E', 'W', 'o'}
        nodes = []
        pos = {}
        for y in range(height):
            if y not in nodes:
                nodes.append([])
            for x in range(width):
                if x != 4 or y == 2:
                    nodes[y].append((x, y))
                    graph.add_node((x, y))
                    pos[(x, y)] = (x, y)

        for y in range(height):
            for x in range(width):
                if x > 0 and (x != 4 and x - 1 != 3) and (x != 5 and x - 1 != 4):
                    graph.add_edge((x, y), (x - 1, y), action='W')
                    graph.add_edge((x - 1, y), (x, y), action='E')
                if y > 0 and x != 4:
                    graph.add_edge((x, y), (x, y - 1), action='S')
                    graph.add_edge((x, y - 1), (x, y), action='N')
        graph.add_edge((3, 2), (4, 2), action='E')
        graph.add_edge((4, 2), (3, 2), action='W')
        graph.add_edge((4, 2), (5, 2), action='E')
        graph.add_edge((5, 2), (4, 2), action='W')
        nx.set_node_attributes(graph, pos, 'pos')
        return graph


def _add_node(graph, col_index, row_index, cell, diagonals, randomise_actions=False, euclidean_dist=True):
    if int(cell) == 1:
        x = int(col_index)
        y = int(row_index)
        node = (x, y)
        nodes = graph.nodes()
        graph.add_node(node, pos=node)
        if (x - 1, y) in nodes:
            graph.add_edge((x - 1, y), node, action='E')
            graph.add_edge(node, (x - 1, y), action='W')
        if (x, y - 1) in nodes:
            graph.add_edge((x, y - 1), node, action='N')
            graph.add_edge(node, (x, y - 1), action='S')
        if diagonals:
            dist = math.sqrt(2) if euclidean_dist else 1
            if (x - 1, y - 1) in nodes:
                graph.add_edge(node, (x - 1, y - 1), action='SW', distance=dist)
                graph.add_edge((x - 1, y - 1), node, action='NE', distance=dist)
            if (x + 1, y - 1) in nodes:
                graph.add_edge(node, (x + 1, y - 1), action='SE', distance=dist)
                graph.add_edge((x + 1, y - 1), node, action='NW', distance=dist)


def generate_grid_world(_map: List[List], diagonals=False, randomise_actions=False, euclidean_dist=True) -> nx.Graph:
    """
    Pass in a gridworld as a list of rows from top to bottom where grid squares with a node are 1 and
    without are 0.

    e.g.  V
          |
          V-V
    Would be [[1, 0], [1, 1]]

    NOTE: for grid worlds to be oriented as expected visually it is easier to define the lists
    making up the grid and call _reverse() - see the examples below

    :param _map: e.g.
    :param diagonals Optional add diagonal edges i.e. NW, NE, SW, SE
    :return:
    """
    graph = nx.empty_graph(0, create_using=nx.DiGraph())

    actions = ['o', 'N', 'E', 'S', 'W']
    if diagonals:
        actions += ['NE', 'SE', 'SW', 'NW']
    graph.graph['actions'] = set(actions)

    for row_index, row in enumerate(_map):
        for col_index, cell in enumerate(row):
            _add_node(graph, col_index, row_index, cell, diagonals, euclidean_dist=euclidean_dist)

    if randomise_actions:
        for node in graph.nodes:
            actions = [e[2]['action'] for e in graph.edges(node, data=True)]
            edges = {(n1, n2): d for n1, n2, d in graph.edges(node, data=True)}
            for e in edges:
                ri = randint(0, len(actions) - 1)
                graph.edges[e]['action'] = actions[ri]
                del actions[ri]
            nx.set_edge_attributes(graph, edges)
    return graph


class GridWorldSimple(GridWorldGraph):
    _map = [[1, 0],
            [1, 1],
            [1, 1],
            [1, 0],
            [1, 0]]
    _map.reverse()


class GridWorldLine(GridWorldGraph):
    _map = [[1, 1, 1, 1]]


class GridWorldUnequalRoomsSmall(GridWorldGraph):
    _map = [
        [1, 1, 0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0],
    ]
    _map.reverse()


class GridWorldUnequalRooms(GridWorldGraph):
    _map = [
        [1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1],

    ]
    _map.reverse()


class GridWorldSixRooms(GridWorldGraph):
    """
    This is the Six Room Grid World from Van Dijk's Thesis
    """
    _map = [
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [0,0,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    _map.reverse()


class GridWorldSixRoomsSmall(GridWorldGraph):
    _map = [
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    ]
    _map.reverse()

