from ..utils.function import generate_graph, find_all_paths_to_dst
from .node import generate_nodes_from_graph, assign_nodes_child, assign_nodes_conflict
from .link import generate_link

class Topo:
    '''
    The Topo class
    '''

    def __init__(self):
        self.topo_dict = {
            'node': {},
            'link': {}
        }
        self.topo_graph = []
        self.path_to_dst = {}

def insert_node(topo, node):
    '''
    Insert a node to the topo

    Args:
        topo (Topo): the topo where the node is added
        node (Node): the node

    Returns:
        Topo: the topo
    '''

    if node.name in topo.topo_dict['node']:
        raise ValueError('The node already exists')

    topo.topo_dict['node'][node.name] = node

def insert_link(topo, link):
    '''
    Insert a link to the topo

    Args:
        topo (Topo): the topo where the link is added
        link (Link): the link

    Returns:
        Topo: the topo
    '''

    if link.name in topo.topo_dict['link']:
        raise ValueError('The link already exists')

    topo.topo_dict['link'][link.name] = link

def generate_topo(size, min_node_amount, max_node_amount, affect_radius, tree_type):
    '''
    Generate the topo

    Args:
        size (int): The size of the grid
        min_node_amount (int): The minimum amount of nodes
        max_node_amount (int): The maximum amount of nodes
        affect_radius (int): The affect radius
        tree_type (str): The type of tree (DAG or TREE)

    Returns:
        topo (Topo): The topo
    '''

    if tree_type not in ['DAG', 'TREE']:
        raise ValueError('The tree type should be DAG or TREE')

    topo = Topo()
    topo.topo_graph = generate_graph(size, min_node_amount, max_node_amount, affect_radius)

    nodes_list = generate_nodes_from_graph(topo.topo_graph)
    for node in nodes_list:
        insert_node(topo, node)

    assign_nodes_child(topo.topo_dict['node'].values(), affect_radius, tree_type)
    assign_nodes_conflict(topo.topo_dict['node'].values())

    links_list = generate_link(topo.topo_dict['node'].values())
    for link in links_list:
        insert_link(topo, link)

    pending_nodes = [node for node in topo.topo_dict['node'].values() if node.type == 'node']

    for node in pending_nodes:
        topo.path_to_dst[node.name] = find_all_paths_to_dst(topo.topo_dict['node']['d'], node)

    return topo

def get_topo_info(topo):
    '''
    Get the topo information

    Args:
        topo (Topo): The topo

    Returns:
        str: The topo information
    '''

    info = ''

    info += '--------------GRAPH---------------\n\n'
    for x in topo.topo_graph:
        info += f'{x}\n'

    info += '\n---------------TOPO---------------\n\n'
    nodes = topo.topo_dict['node'].values()
    links = topo.topo_dict['link'].values()

    for node in nodes:
        info += f'Node: {node.name}\n'
        node = topo.topo_dict['node'][node.name]

        for link in links:
            if link.node['src'] == node:
                info +=  f'  Link: {link.name}' + \
                         f' (Data Rate: {link.data_rate})\n'

    info += '\n-----------PATH AMOUNT------------\n\n'

    for node, paths in topo.path_to_dst.items():
        path = []

        for p in paths:
            path.append([n.name for n in p])

        info += f'Node: {node} (Path Amount: {len(path)})\n'

    return info