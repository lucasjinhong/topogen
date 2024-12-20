from ..utils.error_handler import err_raise
from ..utils.function import graph_matrix_to_dict, replace_graph_elements, find_paths_from_donor_to_all_nodes
from .node import generate_nodes_from_graph, setup_conflict_nodes, find_node_to_dst_by_graph
from .link import generate_links


class Topo:
    def __init__(self):
        self.nodes = {}
        self.links = {}
        self.topo_graph = {}
        self.path_to_dst = {}

def generate_topology_from_graph(graph, tree_type, max_dist_to_connect_nodes, size_of_grid_len, data_rate_formula=None):
    '''
    Generate the topo from the graph

    Args:
        graph (list[list[int]]): The graph of the topo
        tree_type (str): The type of the tree (DAG or TREE)
        max_dist_to_connect_nodes: (float): The maximum distance allowed to connect nodes
        size_of_grid_len (int): The size per grid (meter)
        data_rate_formula (function(distance)): The data rate formula (default is the Shannon Capacity formula)

    Returns:
        Topo: The topo

    Example:
        topo = generate_topology_from_graph([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [1, 0, 0, 0]], 'DAG', 1.5, 10)
    '''

    # error handling
    err_raise(ValueError, 'The graph is empty', graph == [] or [] in graph)
    err_raise(ValueError, 'The tree type should be DAG or TREE', tree_type not in ['DAG', 'TREE'])
    err_raise(ValueError, 'Only Donor can be the root node', graph[0].count(1) != 1)

    topo = Topo()
    topo.topo_graph = graph_matrix_to_dict(graph)
    topo.nodes = generate_nodes_from_graph(topo.topo_graph, max_dist_to_connect_nodes, tree_type)

    if data_rate_formula:
        topo.links = generate_links(topo.nodes, data_rate_formula)
    else:
        topo.links = generate_links(topo.nodes)

    topo.topo_graph = replace_graph_elements(topo.topo_graph, topo.nodes)

    setup_conflict_nodes(topo.nodes)
    find_node_to_dst_by_graph(topo.nodes, topo.topo_graph)
    topo.path_to_dst = find_paths_from_donor_to_all_nodes(topo.nodes)

    return topo

# def get_topo_info(topo):
#     '''
#     Get the topo information

#     Args:
#         topo (Topo): The topo

#     Returns:
#         str: The topo information
#     '''

#     info = ''

#     info += '--------------GRAPH---------------\n\n'
#     for x in topo.topo_graph:
#         info += f'{x}\n'

#     info += '\n---------------TOPO---------------\n\n'
#     nodes = topo.topo_dict['node'].values()
#     links = topo.topo_dict['link'].values()

#     for node in nodes:
#         info += f'Node: {node.name}\n'
#         node = topo.topo_dict['node'][node.name]

#         for link in links:
#             if link.node['src'] == node:
#                 info +=  f'  Link: {link.name}' + \
#                          f' (Data Rate: {link.data_rate})\n'

#     info += '\n-----------PATH AMOUNT------------\n\n'

#     for node, paths in topo.path_to_dst.items():
#         path = []

#         for p in paths:
#             path.append([n.name for n in p])

#         info += f'Node: {node} (Path Amount: {len(path)})\n'

#     return info