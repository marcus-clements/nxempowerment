import logging
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle

from nxempowerment.utils import sigfigs

logger = logging.getLogger(__name__)


def shorten_edge(src, tgt, factor=0.5):
    src = np.array(src)
    tgt = np.array(tgt)
    return src + ((tgt - src) * factor)


def _draw_edge_measure(graph, pos, labels, cmap, node_color, node_size, vmax, vmin):
    """
    Typically edge measure has action probabilities.
    :param cmap:
    :param graph:
    :param labels:
    :param node_color:
    :param node_size:
    :param pos:
    :param vmax:
    :param vmin:
    :return:
    """
    nx.draw_networkx_edges(graph, pos, arrows=False, alpha=0.1, width=1, node_size=node_size)
    edge_measure = nx.get_edge_attributes(graph, graph.graph['edge_measure'])
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_measure, edge_color=edge_colors, label_pos=0.1,
    #                              font_size=8)
    arrowstyle = ArrowStyle("Wedge, tail_width=0.5, shrink_factor=0.1")
    # Shorten the edges and set the width according to the measure
    l_width = []
    for node in graph.nodes:
        edges = []
        e_pos = {node: pos[node]}
        e_width = []
        l_w = 0
        for edge in nx.edges(graph, node):
            print(edge)
            (src, tgt) = edge
            if edge_measure[edge] > 0:
                print(edge_measure[edge])
                edges.append(edge)
                e_pos[tgt] = shorten_edge(pos[src], pos[tgt])
                e_width.append((edge_measure[edge] * 10))

                if src == tgt:
                    l_w = (edge_measure[edge] * 10)
        l_width.append(l_w)

        nx.draw_networkx_edges(graph, e_pos, edges, arrows=True, width=e_width, node_size=50,
                               arrowstyle=arrowstyle)
    nx.draw_networkx_nodes(graph, pos, node_size=node_size, vmin=vmin, vmax=vmax, cmap=cmap, edgecolors='#000000',
                           node_color=node_color, linewidths=l_width)
    nx.draw_networkx_labels(graph, pos, labels, font_size=10)


def plot_graph(graph: nx.Graph,
               filepath: str=None,
               node_color: list=None,
               labels: dict= None,
               title=None,
               figsize=None,
               colorbar=False,
               vmin=None,
               vmax=None,
               node_size=1200,
               actions=False,
               arrows=False,
               format='png',
               *args,
               **kwargs) -> None:

    if figsize is None:
        try:
            figsize = graph.graph['figsize']
        except KeyError:
            figsize = (15, 10)

    plt.close()
    plt.figure(figsize=figsize)
    with_labels = True if labels else False

    edge_labels = None
    edge_colors = None
    if node_color and vmin is None:
        vmin = min(node_color)
        vmax = max(node_color)
    cmap = plt.cm.coolwarm

    pos = nx.get_node_attributes(graph, 'pos')

    if edge_labels is not None:
        nx.draw(G=graph, with_labels=with_labels, pos=pos, node_color=node_color, labels=labels,
                node_size=node_size, label=title, edge_color=edge_colors, width=3, arrows=arrows,
                *args, **kwargs)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    else:
        if 'edge_measure' in graph.graph:
            _draw_edge_measure(graph, pos, labels, cmap, node_color, node_size, vmax, vmin)
        else:
            nx.draw(G=graph, with_labels=with_labels, pos=pos, node_color=node_color, labels=labels,
                    node_size=node_size, label=title, width=1, vmin=vmin, vmax=vmax, cmap=cmap,
                    arrows=arrows, arrowsize=12, *args, **kwargs)

        if 'actions' in graph.graph and actions:
            actions = nx.get_edge_attributes(graph, 'action')
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=actions,
                                         label_pos=0.35, font_size=12)

    plt.title(title)
    plt.draw()
    if colorbar:
        _colorbar(colorbar, cmap, vmin, vmax)

    if filepath is None:
        plt.show()
    else:
        logger.info("Saving plot to %s", filepath)
        if format == 'svg':
            plt.savefig(filepath, format=format, dpi=1200)
        else:
            plt.savefig(filepath, format=format)
    plt.close()


def _colorbar(style, cmap, vmin, vmax):

    if style == "six_room":
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm._A = []
        cbar = plt.colorbar(sm, shrink=0.8, pad=0, aspect=30, fraction=0.08)
        cbar.ax.tick_params(labelsize=40)

    if style == "soho":
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm._A = []
        cbar = plt.colorbar(sm, shrink=0.8, pad=0, aspect=50, fraction=0.06)
        cbar.ax.tick_params(labelsize=50)

    if style == "soho_nodes":
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        sm._A = []
        cbar = plt.colorbar(sm, shrink=0.4, pad=0, aspect=30, fraction=0.13)
        cbar.ax.tick_params(labelsize=30)


def plot_graph_with_measure(graph: nx.Graph,
                            measure_name: str=None,
                            output_filepath: str=None,
                            title=None,
                            figsize=None,
                            num_sigfigs: int=3,
                            colorbar=False,
                            vmin=None,
                            vmax=None,
                            node_size=1200,
                            actions=False,
                            node_names=True,
                            minval=0.001,
                            format='png',
                            *args,
                            **kwargs) -> None:
    """Plog a graph with a measure for each node.

    The measure name must be supplied as a graph attribute called 'measure'.
    Each node must have an attribute with that name and the value of the measure.
    Each node must also have a 'pos' attribute to lay the graph out.
    """
    measure = {}
    pos = {}
    for node, datadict in graph.nodes.items():
        if measure_name:
            val = datadict[measure_name]
            if minval is not None and val < minval:
                val = 0
            measure[node] = val

    node_color = list(nx.get_node_attributes(graph, measure_name).values())
    labels = {}

    for node in graph.nodes:
        measure_str = sigfigs(measure[node], num_sigfigs) if measure_name else ' '
        labels[node] = '{}\n{}'.format(node, measure_str) if node_names else measure_str
    plot_graph(graph=graph, filepath=output_filepath, node_color=node_color, labels=labels, title=title,
               figsize=figsize, colorbar=colorbar, vmin=vmin, vmax=vmax, node_size=node_size, actions=actions,
               format=format, *args, **kwargs)
