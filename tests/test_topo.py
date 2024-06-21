import pytest
from math import ceil, sqrt

from topogen.model.topo import *
from topogen.model.node import Node, insert_child_node
from topogen.model.link import Link

def test_create_topo():
    '''
    Test the Topo class.
    '''

    # Initialize
    topo = Topo()

    # Test the Topo object
    assert topo.topo_dict['node'] == {}
    assert topo.topo_dict['link'] == {}
    assert topo.topo_graph == []
    assert topo.path_to_dst == {}

def test_insert_node():
    '''
    Test the create_node function.
    '''

    # Initalize
    topo = Topo()

    node = Node('1', 'node')
    insert_node(topo, node)

    # Test the node in the topo
    assert node.name in topo.topo_dict['node']
    assert topo.topo_dict['node'][node.name] == node

    # Test if the node is already added
    with pytest.raises(ValueError):
        insert_node(topo, node)

def test_insert_link():
    '''
    Test the insert_link function
    '''

    # Initalize
    topo = Topo()

    node1 = Node('1', 'node')
    node2 = Node('2', 'node')
    insert_child_node(node1, node2)

    link = Link('link1', node1, node2)
    insert_link(topo, link)

    # Test the link in the topo
    assert link.name in topo.topo_dict['link']
    assert topo.topo_dict['link'][link.name] == link

    # Test if the link is already added
    with pytest.raises(ValueError):
        insert_link(topo, link)

def test_generate_topo():
    '''
    Test the generate_topo function
    '''

    # Initialize
    topo_dag = generate_topo(7, ceil(sqrt(7)), 7 // 2, 2, 'DAG')
    topo_tree = generate_topo(7, ceil(sqrt(7)), 7 // 2, 2, 'TREE', topo_dag.topo_graph)

    # Test the topo
    assert len(topo_dag.topo_graph) == 7
    assert len(topo_dag.topo_graph[0]) == 7
    assert topo_dag.topo_graph[0].count('0') == 6
    assert topo_dag.topo_dict['node'] != {}
    assert topo_dag.topo_dict['link'] != {}
    assert topo_dag.path_to_dst != {}

    assert topo_tree.topo_graph ==  topo_dag.topo_graph
    assert topo_tree.topo_dict['node'].keys() == topo_dag.topo_dict['node'].keys()
    for path in topo_tree.path_to_dst.values():
        assert len(path) == 1

    with pytest.raises(ValueError):
        generate_topo(4, 1, 3, 1, 'tst')

def test_get_topo_info():
    '''
    Test the get_topo_info function
    '''

    # Initialize
    topo = Topo()
    topo.topo_graph = [['0', '0', '-1', '0'], ['0', '-1', '0', '0'], ['-1', '0', '0', '0'], ['-1', '-1', '0', '0']]
    nodes_list = generate_nodes_from_graph(topo.topo_graph)
    for node in nodes_list:
        insert_node(topo, node)

    assign_nodes_child(topo.topo_dict['node'].values(), 1, 'DAG')
    assign_nodes_conflict(topo.topo_dict['node'].values())

    links_list = generate_link(topo.topo_dict['node'].values())
    for link in links_list:
        insert_link(topo, link)

    pending_nodes = [node for node in topo.topo_dict['node'].values() if node.type == 'node']

    for node in pending_nodes:
        topo.path_to_dst[node.name] = find_all_paths_to_dst(topo.topo_dict['node']['d'], node)

    # Test the topo info
    info = get_topo_info(topo)
    compare_info = "--------------GRAPH---------------\n\n"
    compare_info += "['0', '0', 'd', '0']\n"
    compare_info += "['0', '1', '0', '0']\n"
    compare_info += "['2', '0', '0', '0']\n"
    compare_info += "['3', '4', '0', '0']\n\n"
    compare_info += "---------------TOPO---------------\n\n"
    compare_info += "Node: d\n"
    compare_info += "  Link: ('d', '1') (Data Rate: 0)\n"
    compare_info += "Node: 1\n"
    compare_info += "  Link: ('1', '2') (Data Rate: 0)\n"
    compare_info += "Node: 2\n"
    compare_info += "  Link: ('2', '3') (Data Rate: 0)\n"
    compare_info += "  Link: ('2', '4') (Data Rate: 0)\n"
    compare_info += "Node: 3\n"
    compare_info += "Node: 4\n\n"
    compare_info += "-----------PATH AMOUNT------------\n\n"
    compare_info += "Node: 1 (Path Amount: 1)\n"
    compare_info += "Node: 2 (Path Amount: 1)\n"
    compare_info += "Node: 3 (Path Amount: 1)\n"
    compare_info += "Node: 4 (Path Amount: 1)\n"

    assert info == compare_info