from random import randint
from math import ceil, sqrt, log10
from collections import deque

from .utils.function import implement_half_duplex_rule
from .model.topo import Topo


TOPO = Topo()

# =======================
# Auto generate method
# =======================
def find_path(node_dict):
    '''
    Find all path to node

    Args:
        node_list (list[obj]): The node object

    return:
        path_to_node (dict): The path to node
    '''

    if '0' not in node_dict:
        raise ValueError('Donor not exist')

    donor = node_dict['0']
    path_to_node = donor.path_to_node
    traversed_node_stack = deque([donor])

    # use DFS to find the path to node
    while traversed_node_stack:
        node = traversed_node_stack.popleft()

        for node_down in node.child_node:
            if node_down.name not in path_to_node:
                path_to_node[node_down.name] = []

            if node == donor:
                path_to_node[node_down.name].append([donor, node_down])
            else:
                for path in path_to_node[node.name]:
                    if path + [node_down] not in path_to_node[node_down.name]:
                        path_to_node[node_down.name].append(path + [node_down])

            traversed_node_stack.append(node_down)

    return donor.path_to_node

def generate_node_automatically(
        min_node_amount = None,
        max_node_amount = None,
        size = 4,
        radiation_radius = 2,
        distance_corresponding = 10,
        tree_type = 'DAG'
    ):
    '''
    Auto generate the node in topo graph

    Args:
        min_node_amount (int): The min node amount in each row | default: ceil(sqrt(graph_size))
        max_node_amount (int): The max node amount in each row | default: size // 2
        size (int): The size of the topo graph | default: 4
        radiation_radius (int): The radiation radius of the IAB node | default: 2
        distance_corresponding (dict): The distance corresponding | default: 10
        tree_type (str): The tree type | default: 'DAG'
    Returns:
        node (list[obj]) : The node object
        graph (list[list[int]]) : The topo graph
    '''

    if not min_node_amount: min_node_amount = ceil(sqrt(size))
    if not max_node_amount: max_node_amount = size // 2

    if size < 4: raise ValueError('Size must be greater than 4')
    elif radiation_radius < 1: raise ValueError('Radiation radius must be greater than 1')
    elif min_node_amount > max_node_amount: raise ValueError('Min node amount must be less than max node amount')
    elif tree_type not in ['DAG', 'TREE']: raise ValueError(f"tree_type must be 'DAG' or 'TREE', not {tree_type}")

    # random generate topo graph

    TOPO.topo_graph_generate(size, min_node_amount, max_node_amount, True)
    TOPO.donor_generate()                                     # generate IAB donor
    TOPO.node_generate(size, radiation_radius, tree_type)     # generate IAB node
    TOPO.topo_graph_generate(size)                            # regenerate topo graph'

    for node in TOPO.topo_dict['node'].values():
        TOPO.child_node_distance_calculate(node, distance_corresponding)

    return TOPO.topo_dict['node'], TOPO.topo_graph

def generate_link_automatically(node_dict, data_rate_function=None):
    '''
    Generate the link in topo graph

    Args:
        node_dict (dict[obj]): The node object
        data_rate_function (function): The data rate function

    Returns:
        link (dict[obj]) : The link object
    '''

    if not data_rate_function:
        data_rate_function = randint(1, 10)

    TOPO.topo_dict['node'] = node_dict
    TOPO.link_generate(data_rate_function)                # generate link
    implement_half_duplex_rule(TOPO.topo_dict['node'])

    return TOPO.topo_dict['link']

# =======================
# Get info method
# =======================
def get_all_info(node_dict, graph = None):
    '''
    Print all the node and link information

    Args:
        node_list (list[obj]): The node object
        link_list (list[obj]): The link object
    '''
    info = ''

    if graph:
        info += '--------------GRAPH---------------\n\n'
        for x in graph:
            info += f'{x}\n'

    info += '\n---------------TOPO---------------\n\n'
    nodes = node_dict.values()

    for node in nodes:
        info += f'Node: {node.name}\n'
        node = node_dict[node.name]

        for link in node.link['down']:
            reserve_time_start = node.link_reserve_time[link.name]['start']
            reserve_time_end = node.link_reserve_time[link.name]['end']

            info +=  f'  Link: {link.name}' + \
                        f' (Data Rate: {link.data_rate}' + \
                        f', Link Conflict: {[l.name for l in link.link_conflict]}' + \
                        f', Reservation Time: [{reserve_time_start}:{reserve_time_end}])\n'

    info += '\n---------------PATH---------------\n\n'

    donor = node_dict['0']

    for link, paths in donor.path_to_node.items():
        path = []

        for p in paths:
            path.append([n.name for n in p])

        info += f'link: {link} (Path: {path})\n'

    info += '\n----------------------------------'

    return info

# not implement yet
def __test_manual():
    print('===========Test manual============')

    topo = Topo()
    topo_dict = {
        'node': {},
        'link': {}
    }

    # add node
    node_dict = topo_dict['node']
    node_dict['0'] = topo.add_node('0', 'donor')
    node_dict['1'] =topo.add_node('1', 'node')
    node_dict['2'] =topo.add_node('2', 'node')
    node_dict['3'] =topo.add_node('3', 'node')
    node_dict['4'] =topo.add_node('4', 'node')

    # add link
    link_dict = topo_dict['link']
    link_dict['0-1'] = topo.add_link('0', '1')
    link_dict['1-2'] = topo.add_link('1', '2')
    link_dict['2-3'] = topo.add_link('2', '3')
    link_dict['3-4'] = topo.add_link('3', '4')

    # add link error
    try:
        topo.add_link('4', '0')
    except AssertionError as e:
        print('--------Test add link error-------\n')
        print(f'Error: {e}')

    # add rule
    topo.initialize_half_duplex_rule(node_dict)

    # find path
    path_to_node = topo.find_path(node_dict)
    donor = node_dict['0']
    donor.path_to_node = path_to_node

    # print(topo)
    info = topo.get_all_info(node_dict, link_dict)
    print(info)

    print('===============End================')

def __test_auto():
    print('\n============Test auto=============')

    fc = lambda x, y: randint(x * 32 * 10**6, y * 32 * 10**6)
    data_rate_function = lambda d: round(32.4 + (31.7 * log10(d)) + (20 * log10(fc(23, 28))), 2)

    node_dict, graph = generate_node_automatically()
    link_dict = generate_link_automatically(node_dict, data_rate_function)
    path_to_node = find_path(node_dict)

    donor = node_dict['0']
    donor.path_to_node = path_to_node

    # print(topo)
    info = get_all_info(node_dict, graph)
    print(info)

    print('===============End================')

if __name__ == '__main__':
    # __test_manual()
    __test_auto()