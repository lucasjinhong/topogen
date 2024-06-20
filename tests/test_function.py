import pytest

from topogen.model.node import Node, insert_child_node, generate_nodes_from_graph
from topogen.utils.function import *


def test_find_all_paths_to_dst():
    '''
    Test the find_all_paths_to_dst function
    '''

    # Create four Node objects
    node1 = Node('1', 'node')
    node2 = Node('2', 'node')
    node3 = Node('3', 'node')
    node4 = Node('4', 'node')

    # Add node2 and node3 as child nodes of node1
    insert_child_node(node1, node2)
    insert_child_node(node1, node3)

    # Add node4 as a child node of node3
    insert_child_node(node3, node4)

    # Add node4 as a child node of node2
    insert_child_node(node2, node4)

    # Test all paths to node4
    path_list = find_all_paths_to_dst(node1, node4)
    assert path_list == [[node1, node2, node4], [node1, node3, node4]]

def test_find_node_childs():
    '''
    Test the find_node_childs function
    '''

    # Initialize
    topo_graph = [['0', '0', '-1', '0'], ['0', '-1', '0', '0'], ['-1', '0', '0', '0'], ['-1', '-1', '0', '0']]
    nodes = {node.name: node for node in generate_nodes_from_graph(topo_graph)}

    # Find the child nodes of node1
    child_nodes = find_node_childs(nodes['d'], nodes.values(), 1)
    assert child_nodes == [nodes['1']]

    # Test the child nodes of node2
    child_nodes = find_node_childs(nodes['2'], nodes.values(), 1)
    assert child_nodes == [nodes['3'], nodes['4']]

def test_calculate_affected_coordinate():
    '''
    Test the calculate_affected_coordinate function
    '''

    # Initialize
    coordinate = (1, 1)

    # Test the affected coordinate
    affected_coordinate = calculate_affected_coordinate(coordinate, 1, 4)
    assert affected_coordinate == {coordinate, (2, 0), (2, 1), (2, 2)}

    # Test the affected coordinate
    affected_coordinate = calculate_affected_coordinate(coordinate, 2, 4)
    assert affected_coordinate == {coordinate, (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (2, 3), (3, 3)}

    coordinate = (2, 2)

    # Test the reverse affected coordinate
    affected_coordinate = calculate_affected_coordinate(coordinate, 1, 4, True)
    assert affected_coordinate == {coordinate, (1, 2), (1, 1), (1, 3)}

    size = 4
    test_cases = [
        (coordinate, 0, size, "affect_radius must be greater than 1 and less than {}".format(size // 2)),
        (coordinate, 5, size, "affect_radius must be greater than 1 and less than {}".format(size // 2)),
    ]

    for coordinate, affect_radius, size, comment in test_cases:
        with pytest.raises(ValueError, match=comment):
            calculate_affected_coordinate(coordinate, affect_radius, size)

def test_generate_graph():
    '''
    Test the generate_graph function
    '''

    # Initialize
    topo_graph = generate_graph(4, 1, 3, 1)

    # Test the graph
    assert len(topo_graph) == 4
    assert len(topo_graph[0]) == 4
    assert topo_graph[0].count('-1') >= 1 and topo_graph[0].count('-1') <= 3

    for row in range(len(topo_graph)):
        for col in range(row):
            if topo_graph[row][col] == '-1':
                parents_coordinate_list = [coordinate for coordinate in calculate_affected_coordinate((row, col), 1, 4, True) if topo_graph[coordinate[0]][coordinate[1]] == '-1']
                assert len(parents_coordinate_list) > 0

    size = 4
    test_cases = [
        (4, 3, 1, 1, "min_node_amount must be less than max_node_amount"),
        (4, -1, 3, 1, "min_node_amount must be greater than 0 and max_node_amount must be greater than 1"),
        (4, 0, 0, 1, "min_node_amount must be greater than 0 and max_node_amount must be greater than 1"),
        (4, 5, 6, 1, "min_node_amount and max_node_amount must be less than size"),
        (4, 1, 5, 1, "min_node_amount and max_node_amount must be less than size"),
        (4, 1, 3, 0, "affect_radius must be greater than 1 and less than {}".format(size // 2)),
        (4, 1, 3, 5, "affect_radius must be greater than 1 and less than {}".format(size // 2)),
    ]
    for size, min_node_amount, max_node_amount, affect_radius, comment in test_cases:
        with pytest.raises(ValueError, match=comment):
            generate_graph(size, min_node_amount, max_node_amount, affect_radius)