import numpy as np

from nxempowerment.empowerment import graph_node_empowerment
from nxempowerment.grid_world import GridWorldSimple


def test_simple_grid_world_1_step():
    """
    The simple grid world is a small grid world consisting of seven nodes:
    O
    OO
    OO
    O
    O

    Note that the nodes are identified as a tuple (x,y) as though the graph
    is a euclidean plane with origin bottom left
    :return:
    """
    gw = GridWorldSimple().graph()
    emp = graph_node_empowerment(gw, 1)
    # With 1 step empowerment, an agent at a node with 1 edge has empowerment of log_2(1) = 0
    # A node with 3 edges empowerment will be log_2(3) = 1.585 (3 dec places)
    expected = {(0,0): 0, (0,1): 1, (0,2): 1.585, (1,2): 1, (0,3): 1.585, (1,3): 1, (0,4): 0}
    np.testing.assert_allclose(list(emp.values()), list(expected.values()), rtol=1E03)


def test_simple_grid_world_2_steps():
    gw = GridWorldSimple().graph()
    emp = graph_node_empowerment(gw, 2)
    expected = {(0,0): 1, (0,1): 2, (0,2): 2.585, (1,2): 2, (0,3): 2.585, (1,3): 2, (0,4): 1.585}
    np.testing.assert_allclose(list(emp.values()), list(expected.values()), rtol=1E03)
