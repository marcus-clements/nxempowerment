import logging
import networkx as nx
import os

from pathlib import Path

from dotenv import load_dotenv

from nxempowerment.empowerment import graph_node_empowerment
from nxempowerment.grid_world import GridWorldSixRooms, GridWorldUnequalRoomsSmall
from nxempowerment.visualize import plot_graph_with_measure

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

output_dir = Path(__file__).parent.parent / os.getenv('OUTPUT_DIR', 'output')

logger.info("Create a small grid world")
gw = GridWorldUnequalRoomsSmall().graph()
logger.info("Actions are %s", gw.graph['actions'])
# Determining a nice figsize is currently trial and error
# Note that the figsize is set as an attribute of the graph which is
# used by plot_graph_with_measure()
gw.graph['figsize'] = (16, 10)
node_emp = graph_node_empowerment(gw, 3)
nx.set_node_attributes(gw, node_emp, '3_step_empowerment')

# plot_graph_with_measure can add node names but when it's a grid
# they aren't very interesting and just confuse the picture

# If plotting interactively e.g. in Pycharm, don't supply an output file path or a format
# plot_graph_with_measure(gw, '3_step_empowerment', node_names=False)
plot_graph_with_measure(graph=gw,
                        measure_name='3_step_empowerment',
                        output_filepath=output_dir / 'small_grid_world_3_step_empowerment.pdf',
                        node_names=False,
                        actions=True,
                        format='pdf')

logger.info("Create a 6 room grid world environment")
gw2 = GridWorldSixRooms().graph()
logger.info("Actions are %s", gw.graph['actions'])
# Determining a nice figsize is currently trial and error
# Note that the figsize is set as an attribute of the graph which is
# used by plot_graph_with_measure()
gw2.graph['figsize'] = (22, 16)
node_emp2 = graph_node_empowerment(gw2, 3)
nx.set_node_attributes(gw2, node_emp2, '3_step_empowerment')

# plot_graph_with_measure(gw, '3_step_empowerment', node_names=False)
plot_graph_with_measure(graph=gw2,
                        measure_name='3_step_empowerment',
                        output_filepath=output_dir / 'six_room_world_3_step_empowerment.pdf',
                        node_names=False,
                        actions=False,
                        format='pdf')
