from random import randint
from math import ceil, sqrt, log10
from collections import deque
import time

from utils.function import implement_half_duplex_rule
from model.topo import Topo


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
            node_down_paths = path_to_node.setdefault(node_down.name, [])

            if node == donor:
                node_down_paths.append([donor, node_down])
            else:
                for path in path_to_node[node.name]:
                    new_path = path + [node_down]
                    if new_path not in node_down_paths:
                        node_down_paths.append(new_path)

            traversed_node_stack.append(node_down)

    return donor.path_to_node

def generate_topo_automatically(
        min_node_amount = None,
        max_node_amount = None,
        size = 4,
        radiation_radius = 1,
        topo_graph = None,
        tree_type = 'DAG',
        distance_corresponding = None,
        data_rate = None
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
        data_rate_function (function): The data rate function | default: randint(1, 10)
    Returns:
        topo_dict (dict[obj]) : The node object
        graph (list[list[int]]) : The topo graph
    '''

    if not min_node_amount: min_node_amount = ceil(sqrt(size))
    if not max_node_amount: max_node_amount = size // 2
    if not data_rate: data_rate = randint(1, 10)
    if not distance_corresponding: distance_corresponding = 10

    if size < 4: raise ValueError('Size must be greater than 4')
    elif radiation_radius < 1: raise ValueError('Radiation radius must be greater than 1')
    elif min_node_amount > max_node_amount: raise ValueError('Min node amount must be less than max node amount')
    elif tree_type not in ['DAG', 'TREE']: raise ValueError(f"tree_type must be 'DAG' or 'TREE', not {tree_type}")

    # random generate topo graph
    TOPO = Topo()

    TOPO.topo_graph_generate(size, min_node_amount, max_node_amount, True, topo_graph)
    TOPO.donor_generate()                                     # generate IAB donor
    TOPO.node_generate(size, radiation_radius, tree_type)     # generate IAB node
    TOPO.topo_graph_generate(size)                            # regenerate topo graph'

    for node in TOPO.topo_dict['node'].values():
        TOPO.child_node_distance_calculate(node, distance_corresponding)

    TOPO.link_generate(data_rate)                        # generate link
    implement_half_duplex_rule(TOPO.topo_dict['node'])
    find_path(TOPO.topo_dict['node'])

    return TOPO.topo_dict, TOPO.topo_graph

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
    print('===============End================')

def __test_auto():
    print('\n============Test auto=============')

    fc = lambda x, y: randint(x * 32 * 10**6, y * 32 * 10**6)
    data_rate_function = lambda d: round(32.4 + (31.7 * log10(d)) + (20 * log10(fc(23, 28))), 2)

    topo_dict_tree = {
        'node': {},
        'link': {}
    }

    topo_dict_dag = {
        'node': {},
        'link': {}
    }

    topo_dict_dag, topo_graph_dag = generate_topo_automatically(distance_corresponding=lambda: 200)
    topo_dict_tree, topo_graph_tree = generate_topo_automatically(tree_type='TREE', topo_graph=topo_graph_dag, data_rate=data_rate_function)

    # print(topo)
    info_dag = get_all_info(topo_dict_dag['node'], topo_graph_dag)
    info_tree = get_all_info(topo_dict_tree['node'], topo_graph_tree)
    print(info_dag)
    print(info_tree)

    print('===============End================')

if __name__ == '__main__':
    # __test_manual()
    __test_auto()