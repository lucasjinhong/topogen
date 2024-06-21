import pytest

from topogen.model.link import *
from topogen.model.node import Node, assign_nodes_child, insert_child_node, generate_nodes_from_graph


def test_create_link():
    '''
    Test the Link class
    '''

    # Create two Node objects
    node1 = Node('1', 'node')
    node2 = Node('2', 'node')

    # Test if the source node not connected to the destination node
    with pytest.raises(ValueError):
        Link('link1', node1, node2)

    # Add node2 as a child node of node1
    insert_child_node(node1, node2)

    # Create a Link object
    link = Link('link1', node1, node2)

    # Test the Link object
    assert link.name == 'link1'
    assert link.data_rate == 0
    assert link.node['src'] == node1
    assert link.node['dst'] == node2

    link = Link('link2', node1, node2, 100)

    assert link.name == 'link2'
    assert link.data_rate == 100

    # Test if the source node and the destination node are the same
    with pytest.raises(ValueError):
        Link('link1', node1, node1)

def test_generate_link():
    '''
    Test the generate_link function
    '''

    # Initialize
    topo_graph = [['0', '0', '-1', '0'], ['0', '-1', '0', '0'], ['-1', '0', '0', '0'], ['-1', '-1', '0', '0']]
    node_dict = {node.name: node for node in generate_nodes_from_graph(topo_graph)}
    assign_nodes_child(node_dict.values(), 1, 'DAG')

    # Test the link
    link_dict = {link.name: link for link in generate_link(node_dict.values())}
    assert link_dict[('d', '1')].node['src'] == node_dict['d']
    assert link_dict[('d', '1')].node['dst'] == node_dict['1']
    assert link_dict[('1', '2')].node['src'] == node_dict['1']
    assert link_dict[('1', '2')].node['dst'] == node_dict['2']
    assert link_dict[('2', '3')].node['src'] == node_dict['2']
    assert link_dict[('2', '3')].node['dst'] == node_dict['3']
    assert link_dict[('2', '4')].node['src'] == node_dict['2']
    assert link_dict[('2', '4')].node['dst'] == node_dict['4']

def test_assign_data_rate():
    '''
    Test the assign_data_rate function
    '''

    # Initialize
    node1 = Node('1', 'node')
    node2 = Node('2', 'node')
    insert_child_node(node1, node2)

    link = Link('link1', node1, node2)

    # Test the data rate
    assert link.data_rate == 0

    assign_data_rate(link, 100)
    assert link.data_rate == 100

    assign_data_rate(link, 200)
    assert link.data_rate == 200