import pytest

from topogen.model.topo import *
from topogen.utils.function import dist_between_coord


def test_generate_topology_from_graph():
    '''
    Test the generate_topology_from_graph function
    '''

    # Test Boundary Cases
    test_cases = [
        ([], 'DAG', 1.5, 10),
        ([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [1, 1, 0, 1]], 'test', 1.5, 10),
        ([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 0], [1, 1, 0, 1]], 'TREE', 1.5, 10),
        ([[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [1, 1, 0, 1]], 'TREE', 1.5, 10)
    ]

    for graph, tree_type, max_dist_to_connect_nodes, size_of_grid_len in test_cases:
        with pytest.raises(ValueError):
            generate_topology_from_graph(graph, tree_type, max_dist_to_connect_nodes, size_of_grid_len)

    graph = [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [1, 1, 0, 1]]
    topo = generate_topology_from_graph(graph, 'DAG', 1.5, 10)
    nodes = topo.nodes
    links = topo.links
    
    assert len(nodes) == 6
    assert len(links) == 6

    assert nodes['5'].node_to_dst == {}
    assert nodes['4'].node_to_dst == {}
    assert nodes['3'].node_to_dst == {nodes['4']: [nodes['4']], nodes['5']: [nodes['5']]}
    assert nodes['2'].node_to_dst == {nodes['3']: [nodes['3']], nodes['4']: [nodes['3']], nodes['5']: [nodes['3']]}
    assert nodes['1'].node_to_dst == {nodes['3']: [nodes['3']], nodes['4']: [nodes['3']], nodes['5']: [nodes['3']]}
    assert nodes['d'].node_to_dst == {nodes['1']: [nodes['1']], nodes['2']: [nodes['2']], nodes['3']: [nodes['1']
                                                    ,nodes['2']], nodes['4']: [nodes['1'], nodes['2']], nodes['5']: [nodes['1'], nodes['2']]}

    assert topo.topo_graph == {0: ['0', 'd', '0', '0'], 
                               1: ['1', '0', '2', '0'], 
                               2: ['0', '3', '0', '0'], 
                               3: ['4', '5', '0', '0']}
    
    dist_formula = lambda dist: dist * 100
    size_of_grid_lens = 10
    topo = generate_topology_from_graph(graph, 'DAG', 1.5, size_of_grid_lens, dist_formula)
    links = topo.links

    assert links[('d', '1')].data_rate_bps == dist_formula(dist_between_coord(nodes['d'].coordinate, nodes['1'].coordinate) * size_of_grid_lens)
    assert links[('d', '2')].data_rate_bps == dist_formula(dist_between_coord(nodes['d'].coordinate, nodes['2'].coordinate) * size_of_grid_lens)

# def test_generate_topo():
#     '''
#     Test the generate_topo function
#     '''

#     # Initialize
#     topo_dag = generate_topo(7, ceil(sqrt(7)), 7 // 2, 2, 'DAG')
#     topo_tree = generate_topo(7, ceil(sqrt(7)), 7 // 2, 2, 'TREE', topo_dag.topo_graph)

#     # Test the topo
#     assert len(topo_dag.topo_graph) == 7
#     assert len(topo_dag.topo_graph[0]) == 7
#     assert topo_dag.topo_graph[0].count('0') == 6
#     assert topo_dag.topo_dict['node'] != {}
#     assert topo_dag.topo_dict['link'] != {}
#     assert topo_dag.path_to_dst != {}

#     assert topo_tree.topo_graph ==  topo_dag.topo_graph
#     assert topo_tree.topo_dict['node'].keys() == topo_dag.topo_dict['node'].keys()
#     for path in topo_tree.path_to_dst.values():
#         assert len(path) == 1

#     with pytest.raises(ValueError):
#         generate_topo(4, 1, 3, 1, 'tst')

# def test_get_topo_info():
#     '''
#     Test the get_topo_info function
#     '''

#     # Initialize
#     topo = Topo()
#     topo.topo_graph = [['0', '0', '-1', '0'], ['0', '-1', '0', '0'], ['-1', '0', '0', '0'], ['-1', '-1', '0', '0']]
#     nodes_list = generate_nodes_from_graph(topo.topo_graph)
#     for node in nodes_list:
#         insert_node(topo, node)

#     assign_nodes_child(topo.topo_dict['node'].values(), 1, 'DAG')
#     assign_nodes_conflict(topo.topo_dict['node'].values())

#     links_list = generate_link(topo.topo_dict['node'].values())
#     for link in links_list:
#         insert_link(topo, link)

#     pending_nodes = [node for node in topo.topo_dict['node'].values() if node.type == 'node']

#     for node in pending_nodes:
#         topo.path_to_dst[node.name] = find_all_paths_to_dst(topo.topo_dict['node']['d'], node)

#     # Test the topo info
#     info = get_topo_info(topo)
#     compare_info = "--------------GRAPH---------------\n\n"
#     compare_info += "['0', '0', 'd', '0']\n"
#     compare_info += "['0', '1', '0', '0']\n"
#     compare_info += "['2', '0', '0', '0']\n"
#     compare_info += "['3', '4', '0', '0']\n\n"
#     compare_info += "---------------TOPO---------------\n\n"
#     compare_info += "Node: d\n"
#     compare_info += "  Link: ('d', '1') (Data Rate: 0)\n"
#     compare_info += "Node: 1\n"
#     compare_info += "  Link: ('1', '2') (Data Rate: 0)\n"
#     compare_info += "Node: 2\n"
#     compare_info += "  Link: ('2', '3') (Data Rate: 0)\n"
#     compare_info += "  Link: ('2', '4') (Data Rate: 0)\n"
#     compare_info += "Node: 3\n"
#     compare_info += "Node: 4\n\n"
#     compare_info += "-----------PATH AMOUNT------------\n\n"
#     compare_info += "Node: 1 (Path Amount: 1)\n"
#     compare_info += "Node: 2 (Path Amount: 1)\n"
#     compare_info += "Node: 3 (Path Amount: 1)\n"
#     compare_info += "Node: 4 (Path Amount: 1)\n"

#     assert info == compare_info