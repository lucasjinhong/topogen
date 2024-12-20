import pytest

from topogen.utils.function import *
from topogen.model.node import generate_nodes_from_graph


# def test_calculate_affected_coordinate():
#     '''
#     Test the calculate_affected_coordinate function
#     '''

#     # Initialize
#     coordinate = (1, 1)

#     # Test the affected coordinate
#     affected_coordinate = calculate_affected_coordinate(coordinate, 1, 4)
#     assert affected_coordinate == {coordinate, (2, 0), (2, 1), (2, 2)}

#     # Test the affected coordinate
#     affected_coordinate = calculate_affected_coordinate(coordinate, 2, 4)
#     assert affected_coordinate == {coordinate, (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2), (2, 3), (3, 3)}

#     coordinate = (2, 2)

#     # Test the reverse affected coordinate
#     affected_coordinate = calculate_affected_coordinate(coordinate, 1, 4, True)
#     assert affected_coordinate == {coordinate, (1, 2), (1, 1), (1, 3)}

#     size = 4
#     test_cases = [
#         (coordinate, 0, size, "affect_radius must be greater than 1 and less than {}".format(size // 2)),
#         (coordinate, 5, size, "affect_radius must be greater than 1 and less than {}".format(size // 2)),
#     ]

#     for coordinate, affect_radius, size, comment in test_cases:
#         with pytest.raises(ValueError, match=comment):
#             calculate_affected_coordinate(coordinate, affect_radius, size)

# def test_generate_graph():
#     '''
#     Test the generate_graph function
#     '''

#     # Initialize
#     topo_graph = generate_graph(4, 1, 3, 1)

#     # Test the graph
#     assert len(topo_graph) == 4
#     assert len(topo_graph[0]) == 4
#     assert topo_graph[0].count('-1') >= 1 and topo_graph[0].count('-1') <= 3

#     for row in range(len(topo_graph)):
#         for col in range(row):
#             if topo_graph[row][col] == '-1':
#                 parents_coordinate_list = [coordinate for coordinate in calculate_affected_coordinate((row, col), 1, 4, True) if topo_graph[coordinate[0]][coordinate[1]] == '-1']
#                 assert len(parents_coordinate_list) > 0

#     for row in topo_graph:
#         assert row.count('0') == 4 - row.count('-1')

#     size = 4
#     test_cases = [
#         (4, 3, 1, 1, "min_node_amount must be less than max_node_amount"),
#         (4, -1, 3, 1, "min_node_amount must be greater than 0 and max_node_amount must be greater than 1"),
#         (4, 0, 0, 1, "min_node_amount must be greater than 0 and max_node_amount must be greater than 1"),
#         (4, 5, 6, 1, "min_node_amount and max_node_amount must be less than size"),
#         (4, 1, 5, 1, "min_node_amount and max_node_amount must be less than size"),
#         (4, 1, 3, 0, "affect_radius must be greater than 1 and less than {}".format(size // 2)),
#         (4, 1, 3, 5, "affect_radius must be greater than 1 and less than {}".format(size // 2)),
#     ]
#     for size, min_node_amount, max_node_amount, affect_radius, comment in test_cases:
#         with pytest.raises(ValueError, match=comment):
#             generate_graph(size, min_node_amount, max_node_amount, affect_radius)

def test_find_paths_from_donor_to_all_nodes():
    '''
    Test the find_paths_from_donor_to_all_nodes function
    '''

    graph = {0: [0, 1, 0, 0], 1: [1, 0, 1, 0], 2: [0, 1, 0, 0], 3: [1, 1, 0, 1]}
    nodes = generate_nodes_from_graph(graph, 1.5, 'DAG')
    path_to_dst = find_paths_from_donor_to_all_nodes(nodes)
    print(path_to_dst)

    assert path_to_dst['d'] == [[nodes['d']]]
    assert path_to_dst['1'] == [[nodes['d'], nodes['1']]]
    assert path_to_dst['2'] == [[nodes['d'], nodes['2']]]
    assert path_to_dst['3'] == [[nodes['d'], nodes['1'], nodes['3']], [nodes['d'], nodes['2'], nodes['3']]]
    assert path_to_dst['4'] == [[nodes['d'], nodes['1'], nodes['3'], nodes['4']], [nodes['d'], nodes['2'], nodes['3'], nodes['4']]]
    assert path_to_dst['5'] == [[nodes['d'], nodes['1'], nodes['3'], nodes['5']], [nodes['d'], nodes['2'], nodes['3'], nodes['5']]]

def test_dist_between_coord():
    '''
    Test the dist_between_coord function
    '''

    coord1 = (0, 0)
    coord2 = (0, 1)
    assert dist_between_coord(coord1, coord2) == 1

    coord1 = (0, 0)
    coord2 = (1, 1)
    assert dist_between_coord(coord1, coord2) == 2 ** 0.5

def test_replace_graph_elements():
    '''
    Test the replace_graph_elements function
    '''

    graph = {0: [0, 1, 0, 0], 1: [1, 0, 1, 0], 2: [0, 1, 0, 0], 3: [1, 1, 0, 1]}
    nodes = generate_nodes_from_graph(graph, 1.5, 'DAG')
    new_graph = replace_graph_elements(graph, nodes)

    assert new_graph == {0: ['0', 'd', '0', '0'],
                         1: ['1', '0', '2', '0'],
                         2: ['0', '3', '0', '0'],
                         3: ['4', '5', '0', '0']}

def test_graph_matrix_to_dict():
    '''
    Test the graph_matrix_to_dict function
    '''

    graph_matrix = [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [1, 1, 0, 1]]
    graph_dict = {0: [0, 1, 0, 0], 1: [1, 0, 1, 0], 2: [0, 1, 0, 0], 3: [1, 1, 0, 1]}

    assert graph_dict == graph_matrix_to_dict(graph_matrix)

def test_get_yaml_data():
    '''
    Test the get_yaml_data function
    '''

    yaml_file = 'tests/test_data/test.yaml'
    yaml_data = get_yaml_data(yaml_file)

    assert yaml_data['bandwith']['value'] == 1000000000
    assert yaml_data['carrier_frequency']['value'] == 23
    assert yaml_data['tx_power']['value'] == 30
    assert yaml_data['noise_coefficient']['value'] == -174
    assert yaml_data['interference']['value'] == 0

def test_info_exchange():
    '''
    Test the info_exchange function
    '''

    graph = {0: [0, 1, 0, 0], 1: [1, 0, 1, 0], 2: [0, 1, 0, 0], 3: [1, 1, 0, 1]}
    nodes = generate_nodes_from_graph(graph, 1.5, 'DAG')

    nodes['d'].received_info = {
        1: [
            {'time': 1, 'src_node': 'd', 'dst_node': '1', 'path':[nodes['1']], 'hops': 1, 'info': 0},
            {'time': 1, 'src_node': 'd', 'dst_node': '2', 'path':[nodes['1']], 'hops': 1, 'info': 0},
            {'time': 1, 'src_node': 'd', 'dst_node': '2', 'path':[nodes['1']], 'hops': 1, 'info': 0}
        ]
    }

    nodes['d'].send_info = [
        {'time': 11, 'src_node': 'd', 'dst_node': '1', 'path':[nodes['1']], 'hops': 1, 'info': 1},
        {'time': 11, 'src_node': 'd', 'dst_node': '2', 'path':[nodes['2']], 'hops': 1, 'info': 2},
        {'time': 11, 'src_node': 'd', 'dst_node': '3', 'path':[nodes['1'], nodes['3']], 'hops': 2, 'info': 3}
    ]

    nodes['1'].send_info = [
        {'time': 11, 'src_node': 'd', 'dst_node': '2', 'path':[nodes['3'], nodes['2']], 'hops': 2, 'info': 32}
    ]

    info_exchange(nodes, 11)

    assert nodes['d'].received_info == {}
    assert nodes['1'].received_info == {11: [{'time': 11, 'src_node': 'd', 'dst_node': '1', 'path':[], 'hops': 1, 'info': 1}]}
    assert nodes['2'].received_info == {11: [{'time': 11, 'src_node': 'd', 'dst_node': '2', 'path':[], 'hops': 1, 'info': 2}]}

    assert nodes['1'].forward_info == [{'time': 11, 'src_node': 'd', 'dst_node': '3', 'path':[nodes['3']], 'hops': 2, 'info': 3}]
    assert nodes['3'].forward_info == [{'time': 11, 'src_node': 'd', 'dst_node': '2', 'path':[nodes['2']], 'hops': 2, 'info': 32}]

    nodes['1'].send_info = [
        {'time': 12, 'src_node': 'd', 'dst_node': '2', 'path':[nodes['3'], nodes['2']], 'hops': 2, 'info': 62}
    ]

    info_exchange(nodes, 12)

    assert nodes['2'].received_info == {11: [
        {'time': 11, 'src_node': 'd', 'dst_node': '2', 'path':[], 'hops': 1, 'info': 2},
        {'time': 11, 'src_node': 'd', 'dst_node': '2', 'path':[], 'hops': 2, 'info': 32}
        ]}

    assert nodes['3'].received_info == {11: [{'time': 11, 'src_node': 'd', 'dst_node': '3', 'path':[], 'hops': 2, 'info': 3}]}

    assert nodes['3'].forward_info == [{'time': 12, 'src_node': 'd', 'dst_node': '2', 'path':[nodes['2']], 'hops': 2, 'info': 62}]

    info_exchange(nodes, 13)

    assert nodes['2'].received_info == {
        11: [
            {'time': 11, 'src_node': 'd', 'dst_node': '2', 'path':[], 'hops': 1, 'info': 2},
            {'time': 11, 'src_node': 'd', 'dst_node': '2', 'path':[], 'hops': 2, 'info': 32}],
        12: [{'time': 12, 'src_node': 'd', 'dst_node': '2', 'path':[], 'hops': 2, 'info': 62}]
        }