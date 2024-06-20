from ..utils.function import find_node_childs


class Node:
    def __init__(self, name, node_type):
        '''
        Create a new instance of the Node class

        Args:
            name (str): the name of the node
            type_ (str): the type of the node
        '''

        if node_type not in ['donor', 'node']:
            raise ValueError('The node type must be either "donor" or "node"')
        elif name == '':
            raise ValueError('The node name cannot be empty')
        elif type(name) != str:
            raise ValueError('The node name must be a string')

        self.name = name
        self.type = node_type
        self.coordinate = {}                 # coordinate of the node

        self.parents_node = []               # parent node of the node
        self.childs_node = []                # child nodes of the node
        self.conflict_node = []              # conflict nodes of the node

def insert_child_node(node, child_node):
    '''
    Add a child node to the node

    Args:
        node (Node): the node where the child node is added
        child_node (Node): the child node
    '''

    if node == child_node:
        raise ValueError('The node and the child node cannot be the same')
    elif child_node in node.childs_node:
        raise ValueError('The child node already exists')

    node.childs_node.append(child_node)
    child_node.parents_node.append(node)

def insert_conflict_node(node1, node2):
    '''
    Insert the conflict node

    Args:
        node1 (Node): the first node
        node2 (Node): the second node
    '''

    if node2 in node1.conflict_node:
        raise ValueError('The conflict node already exists')

    node1.conflict_node.append(node2)
    node2.conflict_node.append(node1)

def assign_coordinate(node, x, y):
    '''
    Assign the coordinate to the node

    Args:
        node (Node): the node
        x (int): the x coordinate
        y (int): the y coordinate
    '''

    if x < 0 or y < 0:
        raise ValueError('The coordinate must be positive')

    node.coordinate['x'] = x
    node.coordinate['y'] = y

def generate_nodes_from_graph(topo_graph):
    '''
    Generate the node from the topo graph

    Args:
        topo_graph (list[list]): The topo graph

    Returns:
        nodes (list[Node]): The nodes
    '''

    if topo_graph == []:
        raise ValueError('The topo graph is empty')

    #generate donors
    nodes = [Node('d', 'donor')]

    for i in range(1, len(topo_graph)):
        for j in range(len(topo_graph[i])):
            if topo_graph[i][j] == '-1':
                nodes.append(Node(str(len(nodes)), 'node'))

    topo_graph = assign_nodes_position(nodes, topo_graph)

    return nodes

def assign_nodes_child(nodes, affect_radius):
    '''
    Assign the child nodes to the nodes

    Args:
        nodes (list[Node]): The nodes
    '''

    for node in nodes:
        childs_node = find_node_childs(node, nodes, affect_radius)

        for child_node in childs_node:
            insert_child_node(node, child_node)

def assign_nodes_position(nodes, topo_graph):
    '''
    Assign the node position

    Args:
        nodes (list[Node]): The nodes
        topo_graph (list[list]): The topo graph

    Returns:
        topo_graph (list[list]): The topo graph
    '''

    unassigned_nodes = [node for node in nodes if node.coordinate == {}]
    i = 0

    while i < len(topo_graph) and unassigned_nodes != []:
        for j in range(len(topo_graph[i])):
            if topo_graph[i][j] == '-1':
                node = unassigned_nodes.pop(0)
                topo_graph[i][j] = node.name
                assign_coordinate(node, i, j)

            if unassigned_nodes == []:
                break

        i += 1

    return topo_graph

def assign_nodes_conflict(nodes):
    '''
    Assign the conflict nodes to the nodes

    Args:
        nodes (list[Node]): The nodes
    '''

    for node in nodes:
        for child_node in node.childs_node:
            insert_conflict_node(node, child_node)