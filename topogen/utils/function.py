from math import sqrt
from copy import deepcopy
from yaml import safe_load


def find_paths_from_donor_to_all_nodes(nodes):
    '''
    Find the path from the donor node to all the nodes

    Args:
        nodes (dict{str: Node}): The nodes

    Returns:
        paths (dict{str: list[Node]}): The path from the donor node to all the nodes
    '''

    donor = nodes['d']
    paths = {}

    for node in nodes.values():
        path_to_node = []
        path = [donor]

        def dfs(n):
            if n == node:
                path_to_node.append(path.copy())
                return

            for child in n.children:
                path.append(child)
                dfs(child)
                path.pop()

        dfs(donor)
        paths[node.name] = path_to_node

    return paths

# def calculate_affected_coordinate(coordinate, affect_radius, size, reverse=False):
#     '''
#     Calculate the affected coordinate

#     Args:
#         coordinate (tuple): The coordinate
#         affect_radius (int): The affect radius
#         size (int): The size of the topo graph

#     Returns:
#         affected_coordinate (set(tuple)): The affected coordinate
#     '''

#     if affect_radius < 1 or affect_radius > size // 2:
#         raise ValueError('affect_radius must be greater than 1 and less than {}'.format(size // 2))

#     affected_coordinate = {coordinate}
#     x = coordinate[0]
#     y = coordinate[1]

#     if reverse:
#         for i in range(1, affect_radius + 1):
#             if x - i >= 0:
#                 affected_coordinate.add((x - i, y))

#                 for j in range(1, affect_radius + 1):
#                     if y - j >= 0:
#                         affected_coordinate.add((x - i, y - j))
#                     if y + j < size:
#                         affected_coordinate.add((x - i, y + j))
#     else:
#         for i in range(1, affect_radius + 1):
#             if x + i < size:
#                 affected_coordinate.add((x + i, y))

#                 for j in range(1, affect_radius + 1):
#                     if y - j >= 0:
#                         affected_coordinate.add((x + i, y - j))
#                     if y + j < size:
#                         affected_coordinate.add((x + i, y + j))

#     return affected_coordinate

# def generate_graph(size, min_node_amount, max_node_amount, affect_radius):
#     '''
#     Generate the topo graph

#     Args:
#         size (int): The size of the topo graph per row
#         min_node_amount (int): The min node amount in each row
#         max_node_amount (int): The max node amount in each row
#         affect_radius (int): The affect radius that a node can connect with other nodes

#     Returns:
#         topo_graph (list[list]): The topo graph
#     '''

#     if min_node_amount > max_node_amount:
#         raise ValueError('min_node_amount must be less than max_node_amount')
#     elif min_node_amount < 0 or max_node_amount < 1:
#         raise ValueError('min_node_amount must be greater than 0 and max_node_amount must be greater than 1')
#     elif min_node_amount > size or max_node_amount > size:
#         raise ValueError('min_node_amount and max_node_amount must be less than size')
#     elif affect_radius < 1 or affect_radius > size // 2:
#         raise ValueError('affect_radius must be greater than 1 and less than {}'.format(size // 2))

#     topo_graph = {i: ['0'] * size for i in range(size)}

#     left_limit = size // 4 * 1
#     right_limit = size // 4 * 2
#     first_row_position = randint(left_limit, right_limit)
#     topo_graph[0][first_row_position] = '-1'

#     affected_coordinate = calculate_affected_coordinate((0, first_row_position), affect_radius, size)

#     # generate the nodes
#     for row in range(1, size):
#         node_amount = randint(min_node_amount, max_node_amount)

#         for position in sample(range(size), node_amount):
#             if (row, position) in affected_coordinate:
#                 topo_graph[row][position] = '-1'
#                 affected_coordinate |= calculate_affected_coordinate((row, position), affect_radius, size)

#     return topo_graph

def dist_between_coord(coord1, coord2):
    '''
    Calculate the distance between two coordinates

    Args:
        coord1 (tuple): The first coordinate
        coord2 (tuple): The second coordinate

    Returns:
        dist (int): The distance
    '''

    return sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def replace_graph_elements(graph, nodes):
    '''
    Replace the int elements with the nodes name in the topo graph

    Args:
        graph (dict[list]): The topo graph
        nodes (dict{str: Node}): The nodes

    Return:
        new_graph (dict[list]): The graph
    '''

    new_graph = deepcopy(graph)

    for key, value in new_graph.items():
        for j in range(len(value)):
            if value[j] == 0:
                value[j] = '0'
            elif value[j] == 1:
                node = [node for node in nodes.values() if node.coordinate == (key, j)]

                if node:
                    value[j] = node[0].name
                else:
                    value[j] = '0'

    return new_graph

def graph_matrix_to_dict(graph_matrix):
    '''
    Convert the matrix to the dictionary

    Args:
        graph_matrix (list[list[int]]): The matrix

    Returns:
        graph_dict (dict{int:list[int]}): The dictionary
    '''
    graph_dict = {}

    for i in range(len(graph_matrix)):
        graph_dict[i] = graph_matrix[i]

    return graph_dict

def get_yaml_data(file_path):
    '''
    Get the data from the yaml file

    Args:
        file_path (str): file path
    '''

    with open(file_path, 'r') as file:
        data = safe_load(file)

    return data

def info_exchange(nodes, time):
    '''
    Exchange the information between nodes.
    The exchange mechanism propagates information one hop at a time. 
    Therefore, if the destination node is two hops away from the source node, 
    the information will reach the destination after two propagation steps.
    
    Args:
        nodes (dict{str: Node}): The nodes
        time (int): time to exchange the information

    Returns:
        None

    Info:
        The info format should be like this:

        info =  {
                    time: 't',
                    src: 'src_node',
                    dst: 'dst_node',
                    path: ['node1', ..., 'dst_node'],   # should setup yourself
                    hops: 'len(path)',
                    info: {info}
               }

        The last element of the path should be the destination node
    '''

    for node in nodes.values():
        if node.received_info.get(time - 10):
            del node.received_info[time - 10]

        satisfied_info = [i for i in node.send_info if i['time'] == time]
        satisfied_info += [i for i in node.forward_info if i['time'] == time - i['hops'] + len(i['path'])]

        node.send_info = list(filter(lambda i: i['time'] != time, node.send_info))
        node.forward_info = list(filter(lambda i: i['time'] != time - i['hops'] + len(i['path']), node.forward_info))

        for info in satisfied_info:
            dst_node = info['path'].pop(0)

            if info['path'] == []:
                dst_node.received_info.setdefault(info['time'], []).append(info)
            else:
                dst_node.forward_info.append(info)