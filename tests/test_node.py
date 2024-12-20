import pytest

from topogen.model.node import *
from topogen.utils.function import replace_graph_elements


def test_create_node():
    '''
    Test the Node class.
    '''

    node = Node('1', 'node')

    assert node.name == '1'
    assert node.type == 'node'

    test_cases = [
        ('1', 'test', 'The node type must be either "donor" or "node"'),
        ('', 'node', 'The node name cannot be empty'),
        (1, 'node', 'The node name must be a string')
    ]

    for name, node_type, comment in test_cases:
        with pytest.raises(ValueError, match=comment):
            Node(name, node_type)

def test_generate_node_from_graph():
    '''
    Test the generate_node_from_graph function.
    '''

    topo_graph = {0: [0, 1, 0, 0], 1: [1, 0, 1, 0], 2: [0, 1, 0, 0], 3: [1, 1, 0, 1]}
    nodes = generate_nodes_from_graph(topo_graph, 1.5, 'DAG')

    assert nodes['d'].name == 'd'
    assert nodes['d'].type == 'donor'
    assert nodes['d'].coordinate == (0, 1)
    assert nodes['d'].children == [nodes['1'], nodes['2']]

    assert nodes['1'].name == '1'
    assert nodes['1'].type == 'node'
    assert nodes['1'].coordinate == (1, 0)
    assert nodes['1'].children == [nodes['3']]

    assert nodes['2'].name == '2'
    assert nodes['2'].type == 'node'
    assert nodes['2'].coordinate == (1, 2)
    assert nodes['2'].children == [nodes['3']]

    assert nodes['1'].parents == [nodes['d']]
    assert nodes['2'].parents == [nodes['d']]
    assert nodes['3'].parents == [nodes['1'], nodes['2']]

    assert len(nodes) == 6

def test_setup_conflict_nodes():
    '''
    Test the setup_conflict_nodes function.
    '''

    topo_graph = {0: [0, 1, 0, 0], 1: [1, 0, 1, 0], 2: [0, 1, 0, 0], 3: [1, 1, 0, 1]}
    nodes = generate_nodes_from_graph(topo_graph, 1.5, 'DAG')
    setup_conflict_nodes(nodes)

    assert set(nodes['d'].conflict_nodes) == set([nodes['1'], nodes['2']])
    assert set(nodes['1'].conflict_nodes) == set([nodes['d'], nodes['2'], nodes['3']])
    assert set(nodes['2'].conflict_nodes) == set([nodes['d'], nodes['1'], nodes['3']])
    assert set(nodes['3'].conflict_nodes) == set([nodes['1'], nodes['2'], nodes['4'], nodes['5']])
    assert set(nodes['4'].conflict_nodes) == set([nodes['3']])

def test_find_node_to_dst_by_graph():
    '''
    Test the find_node_to_dst_by_graph function.
    '''

    topo_graph = {0: [0, 1, 0, 0], 1: [1, 0, 1, 0], 2: [0, 1, 0, 0], 3: [1, 1, 0, 1]}
    nodes = generate_nodes_from_graph(topo_graph, 1.5, 'DAG')
    topo_graph = replace_graph_elements(topo_graph, nodes)
    find_node_to_dst_by_graph(nodes, topo_graph)

    assert nodes['5'].node_to_dst == {}
    assert nodes['4'].node_to_dst == {}
    assert nodes['3'].node_to_dst == {nodes['4']: [nodes['4']], nodes['5']: [nodes['5']]}
    assert nodes['2'].node_to_dst == {nodes['3']: [nodes['3']], nodes['4']: [nodes['3']], nodes['5']: [nodes['3']]}
    assert nodes['1'].node_to_dst == {nodes['3']: [nodes['3']], nodes['4']: [nodes['3']], nodes['5']: [nodes['3']]}
    assert nodes['d'].node_to_dst == {nodes['1']: [nodes['1']], nodes['2']: [nodes['2']], nodes['3']: [nodes['1']
                                                    ,nodes['2']], nodes['4']: [nodes['1'], nodes['2']], nodes['5']: [nodes['1'], nodes['2']]}