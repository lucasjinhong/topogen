from model.link import Link
from model.node import Node


def add_link(node_up, node_down, data_rate):
    '''
    Add link into topo

    Args:
        node_up (Node): The up node
        node_down (Node): The down node

        advanced:
            data_rate_function (function): The data rate function

    Returns:
        link (obj): Link object
    '''

    if node_down.type == 'donor':
        raise ValueError(f'{node_down} is donor, cannot be down node')

    link_name = f'{node_up.name}-{node_down.name}'

    if type(data_rate) == int:
        link_rate = data_rate
    else:
        child_node_distance = node_up.child_node_distance[node_down.name]
        link_rate = data_rate(int(child_node_distance))

    if node_down not in set(node_up.child_node):
        node_up.child_node.append(node_down)

    link = Link(link_name, node_up, node_down, link_rate)

    node_up.link['down'].append(link)
    node_down.link['up'].append(link)
    node_up.link_reserve_time[link.name] = {
        'start': 0,
        'end': 0
    }

    return link

def add_node(node_name, node_type, coordinate=None):
    '''
    Add node into topo

    Args:
        name (str): Node name
        type (str): Node type (IAB donor or IAB node)
        coordinate (dict): Coordinate of the node
        {'x': int, 'y': int}

    Returns:
        node (obj): Node object
    '''

    if node_type not in ['donor', 'node']:
        raise ValueError(f'{node_type} is not a valid type, ex.(donor|node)')
    elif node_type == 'donor' and node_name != '0':
        raise ValueError('Donor must be 0')

    node = Node(node_name, node_type, coordinate)

    return node

def implement_half_duplex_rule(node_dict):
    '''
    Initialize the half duplex rule

    Args:
        node_dict (dict): The node dict
    '''

    for node in node_dict.values():
        links = node.link['down'] + node.link['up']

        # check if link is conflict with other link
        for link in links:
            conflict_links = [l for l in links if l != link]
            link.link_conflict.extend(conflict_links)