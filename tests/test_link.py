import pytest

from topogen.model.link import *
from topogen.model.node import generate_nodes_from_graph, Node
from topogen.config.config import DATA_RATE_BPS_FORMULA
from topogen.utils.function import dist_between_coord


def test_create_link():
    '''
    Test the Link class
    '''

    node1 = Node('1', 'node')
    node2 = Node('2', 'node')

    # Test if the source node not connected to the destination node
    with pytest.raises(ValueError):
        Link('link1', node1, node2)

    node1.children.append(node2)
    node2.parents.append(node1)

    link = Link('link1', node1, node2)

    assert link.name == 'link1'
    assert link.data_rate_bps == 0
    assert link.src_node == node1
    assert link.dst_node == node2

    link = Link('link2', node1, node2, 100)

    assert link.name == 'link2'
    assert link.data_rate_bps == 100

    # Test if the source node and the destination node are the same
    with pytest.raises(ValueError):
        Link('link1', node1, node1)

def test_generate_links():
    '''
    Test the generate_link function
    '''

    topo_graph = {0: [0, 1, 0, 0], 1: [1, 0, 1, 0], 2: [0, 1, 0, 0], 3: [1, 1, 0, 1]}
    nodes = generate_nodes_from_graph(topo_graph, 1.5, 'DAG')
    links = generate_links(nodes)

    assert links[('d', '1')].src_node == nodes['d']
    assert links[('d', '2')].src_node == nodes['d']
    assert links[('1', '3')].src_node == nodes['1']
    assert links[('2', '3')].src_node == nodes['2']

    assert links[('d', '1')].dst_node == nodes['1']
    assert links[('d', '2')].dst_node == nodes['2']
    assert links[('1', '3')].dst_node == nodes['3']
    assert links[('2', '3')].dst_node == nodes['3']

    assert links[('d', '1')].data_rate_bps == DATA_RATE_BPS_FORMULA(dist_between_coord(nodes['d'].coordinate, nodes['1'].coordinate))
    assert links[('d', '2')].data_rate_bps == DATA_RATE_BPS_FORMULA(dist_between_coord(nodes['d'].coordinate, nodes['2'].coordinate))

    dist_formula = lambda dist: dist * 100
    links = generate_links(nodes, dist_formula)

    assert links[('d', '1')].data_rate_bps == dist_formula(dist_between_coord(nodes['d'].coordinate, nodes['1'].coordinate))
    assert links[('d', '2')].data_rate_bps == dist_formula(dist_between_coord(nodes['d'].coordinate, nodes['2'].coordinate))