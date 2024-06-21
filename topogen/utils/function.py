from re import sub
from random import sample, randint


def find_all_paths_to_dst(src, dst):
    '''
    Find the path to the destination

    Args:
        src (str): the source node
        dst (str): the destination node

    Returns:
        paths_list (list[list]): the path to the destination
    '''

    paths_list = []
    path = [src]

    def dfs(node):
        if node == dst:
            paths_list.append(path.copy())
            return

        for child_node in node.childs_node:
            path.append(child_node)
            dfs(child_node)
            path.pop()

    dfs(src)

    return paths_list

def find_node_childs(target_node, nodes, affect_radius):
    '''
    Find the child nodes pf the target node

    Args:
        target_node (Node): The target node
        affect_radius (int): The affect radius
        nodes (list[Node]): The nodes in the topo

    Returns:
        child_nodes (list[Node]): The child nodes
    '''

    child_nodes = []

    x = target_node.coordinate['x']
    y = target_node.coordinate['y']

    for node in nodes:
        x_child = node.coordinate['x']
        y_child = node.coordinate['y']

        if x_child - x > 0 and x_child - x <= affect_radius and abs(y_child - y) <= affect_radius and node != target_node:
            child_nodes.append(node)

    return child_nodes

def calculate_affected_coordinate(coordinate, affect_radius, size, reverse=False):
    '''
    Calculate the affected coordinate

    Args:
        coordinate (tuple): The coordinate
        affect_radius (int): The affect radius
        size (int): The size of the topo graph

    Returns:
        affected_coordinate (set(tuple)): The affected coordinate
    '''

    if affect_radius < 1 or affect_radius > size // 2:
        raise ValueError('affect_radius must be greater than 1 and less than {}'.format(size // 2))

    affected_coordinate = {coordinate}
    x = coordinate[0]
    y = coordinate[1]

    if reverse:
        for i in range(1, affect_radius + 1):
            if x - i >= 0:
                affected_coordinate.add((x - i, y))

                for j in range(1, affect_radius + 1):
                    if y - j >= 0:
                        affected_coordinate.add((x - i, y - j))
                    if y + j < size:
                        affected_coordinate.add((x - i, y + j))
    else:
        for i in range(1, affect_radius + 1):
            if x + i < size:
                affected_coordinate.add((x + i, y))

                for j in range(1, affect_radius + 1):
                    if y - j >= 0:
                        affected_coordinate.add((x + i, y - j))
                    if y + j < size:
                        affected_coordinate.add((x + i, y + j))

    return affected_coordinate

def generate_graph(size, min_node_amount, max_node_amount, affect_radius):
    '''
    Generate the topo graph

    Args:
        size (int): The size of the topo graph per row
        min_node_amount (int): The min node amount in each row
        max_node_amount (int): The max node amount in each row
        affect_radius (int): The affect radius that a node can connect with other nodes

    Returns:
        topo_graph (list[list]): The topo graph
    '''

    if min_node_amount > max_node_amount:
        raise ValueError('min_node_amount must be less than max_node_amount')
    elif min_node_amount < 0 or max_node_amount < 1:
        raise ValueError('min_node_amount must be greater than 0 and max_node_amount must be greater than 1')
    elif min_node_amount > size or max_node_amount > size:
        raise ValueError('min_node_amount and max_node_amount must be less than size')
    elif affect_radius < 1 or affect_radius > size // 2:
        raise ValueError('affect_radius must be greater than 1 and less than {}'.format(size // 2))

    topo_graph = [['0'] * size for _ in range(size)]

    left_limit = size // 4 * 1
    right_limit = size // 4 * 2
    first_row_position = randint(left_limit, right_limit)
    topo_graph[0][first_row_position] = '-1'

    affected_coordinate = calculate_affected_coordinate((0, first_row_position), affect_radius, size)

    # generate the nodes
    for row in range(1, size):
        node_amount = randint(min_node_amount, max_node_amount)

        for position in sample(range(size), node_amount):
            if (row, position) in affected_coordinate:
                topo_graph[row][position] = '-1'
                affected_coordinate |= calculate_affected_coordinate((row, position), affect_radius, size)

    return topo_graph

def replace_graph_elements(topo_graph, target_elements, replace_elements):
    '''
    Replace the target elements with the replace elements in the topo graph

    Args:
        topo_graph (list[list]): The topo graph
        target_elements (set): The target elements
        replace_elements (set): The replace elements

    Returns:
        topo_graph (list[list]): The topo graph
    '''
    graph = topo_graph.copy()

    for i in range(len(graph)):
        graph[i] = list(map(lambda x: sub(target_elements, replace_elements, x), graph[i]))

    return graph