import pytest

from topogen.model.node import *
from topogen.utils.function import generate_graph


def test_create_node():
    '''
    Test the Node class.
    '''

    # Initialize
    node = Node('1', 'node')

    # Test the Node object
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

def test_insert_child_node():
    '''
    Test the insert_child_node function.
    '''

    # Initialize
    node1 = Node('1', 'node')
    node2 = Node('2', 'node')
    insert_child_node(node1, node2)

    # Test the child node of node1
    assert node2 in node1.childs_node

    test_cases = [
        (node1, node2, 'The child node already exists'),
        (node1, node1, 'The node and the child node cannot be the same')
    ]

    for node1, node2, comment in test_cases:
        with pytest.raises(ValueError, match=comment):
            insert_child_node(node1, node2)

def test_insert_conflict_node():
    '''
    Test the insert_conflict_node function.
    '''

    # Initialize
    node1 = Node('1', 'node')
    node2 = Node('2', 'node')
    insert_conflict_node(node1, node2)

    # Test the conflict node of node1
    assert node2 in node1.conflict_node

    # Test if the conflict node is already added
    with pytest.raises(ValueError):
        insert_conflict_node(node1, node2)

def test_assign_coordinate():
    '''
    Test the assign_coordinate function.
    '''

    # Initialize
    node = Node('1', 'node')
    assign_coordinate(node, 1, 2)

    # Test the coordinate of the node
    assert node.coordinate == {'x': 1, 'y': 2}

    # Test if x coordinate is negative
    with pytest.raises(ValueError):
        assign_coordinate(node, -1, 2)

def test_generate_nodes_from_graph():
    '''
    Test the generate_nodes_from_graph function
    '''

    # Initalize
    topo_graph = [['0', '0', '-1', '0'], ['0', '-1', '0', '0'], ['-1', '0', '0', '0'], ['-1', '-1', '0', '0']]
    node_dict = {node.name: node for node in generate_nodes_from_graph(topo_graph)}

    # Test the nodes
    assert node_dict['d'].name == 'd'
    assert node_dict['d'].type == 'donor'
    assert node_dict['1'].name == '1'
    assert node_dict['1'].type == 'node'

    # Test if the topo graph is empty
    topo_graph = []
    with pytest.raises(ValueError):
        generate_nodes_from_graph(topo_graph)

def test_assign_nodes_child():
    '''
    Test the assign_nodes_child function
    '''

    # Initialize
    topo_graph = [['0', '0', '-1', '0'], ['0', '-1', '0', '0'], ['-1', '0', '0', '0'], ['-1', '-1', '0', '0']]
    node_dict = {node.name: node for node in generate_nodes_from_graph(topo_graph)}

    # Test the nodes child
    assign_nodes_child(node_dict.values(), 1)
    assert node_dict['d'].childs_node == [node_dict['1']]
    assert node_dict['1'].childs_node == [node_dict['2']]
    assert node_dict['2'].childs_node == [node_dict['3'], node_dict['4']]
    assert node_dict['3'].childs_node == []
    assert node_dict['4'].childs_node == []

def test_assign_nodes_position():
    '''
    Test the assign_nodes_position function
    '''

    #Initalize
    node1 = Node('1', 'node')

    topo_graph = generate_graph(4, 1, 3, 1)
    nodes = [node1]

    # Test the nodes position
    assign_nodes_position(nodes, topo_graph)
    assert node1.coordinate['x'] == 0 and node1.coordinate['y'] >= 1 and node1.coordinate['y'] <= 3

def test_assign_nodes_conflict():
    '''
    Test the assign_nodes_conflict function
    '''

    # Initialize
    node1 = Node('1', 'node')
    node2 = Node('2', 'node')
    node3 = Node('3', 'node')
    node4 = Node('4', 'node')

    insert_child_node(node1, node2)
    insert_child_node(node1, node3)
    insert_child_node(node3, node4)

    # Test the conflict nodes
    assign_nodes_conflict([node1, node2, node3, node4])
    assert node1.conflict_node == [node2, node3]
    assert node2.conflict_node == [node1]
    assert node3.conflict_node == [node1, node4]
    assert node4.conflict_node == [node3]