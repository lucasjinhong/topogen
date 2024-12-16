# from ..utils.function import find_node_childs
from ..utils.function import dist_between_coord
from ..utils.error_handler import err_raise


class Node:
    def __init__(self, name, node_type):
        '''
        Create a new instance of the Node class

        Args:
            name (str): the name of the node
            node_type (str): the type of the node
        '''

        # error handling
        err_raise(ValueError, 'The node type must be either "donor" or "node"', node_type not in ['donor', 'node'])
        err_raise(ValueError, 'The node name cannot be empty', name == '')
        err_raise(ValueError, 'The node name must be a string', type(name) != str)

        self.name = name
        self.type = node_type
        self.coordinate = ()

        self.parents = []
        self.children = []
        self.links = []
        self.conflict_nodes = []

        self.node_to_dst = {}               # the next node to the destination ex. {node3: [node1, node2]}
        self.received_info = {}             # the received information while distributed ex. {'t':{info}}
        self.forward_info = {}              # the information to be forwarded ex. {'t':{info}}

def setup_conflict_nodes(nodes):
    '''
    Setup the conflict links

    Args:
        nodes (list[Node]): The nodes

    Returns:
        None
    '''

    for node in nodes:
        for parent in node.parents:
            node.conflict_nodes.append(parent)

        for child in node.children:
            node.conflict_nodes.append(child)

            for sibling in child.parents:
                if sibling != node:
                    node.conflict_nodes.append(sibling)

def generate_nodes_from_graph(graph, max_dist_to_connect_nodes, tree_type):
    '''
    Generate the node from the graph and assign the coordinate, parents, children to the nodes
    The node without parents will exclude from the nodes, except the donor

    Args:
        graph (dict{int:list[int]}): The graph
        max_dist_to_connect_nodes (float): The maximum distance to connect nodes
        tree_type (str): The type of the tree (DAG or TREE)

    Returns:
        nodes (dict{str: Node}): the nodes
    '''

    nodes = {}
    donor = Node('d', 'donor')
    donor.coordinate = (0, graph[0].index(1))
    nodes['d'] = donor

    queue = [donor]
    existed_coordinate = [donor.coordinate]

    while queue:
        node = queue.pop(0)

        for i in range(node.coordinate[0] + 1, len(graph)):
            for j in range(len(graph[i])):
                if graph[i][j] == 1 and dist_between_coord(node.coordinate, (i, j)) <= max_dist_to_connect_nodes:
                    if (i, j) not in existed_coordinate:
                        child_node = Node(str(len(nodes)), 'node')
                        child_node.coordinate = (i, j)
                        existed_coordinate.append(child_node.coordinate)

                        nodes[child_node.name] = child_node
                        queue.append(child_node)

                    node.children.append(child_node)
                    child_node.parents.append(node)

    return nodes

# def assign_nodes_child(nodes, graph, max_dist_to_connect_nodes, tree_type):
#     '''
#     Assign the child nodes to the nodes

#     Args:
#         nodes (dict): The nodes
#         graph (dict[list]): The graph
#         max_dist_to_connect_nodes (int): The maximum distance to connect nodes
#         tree_type (str): The type of the tree (DAG or TREE)
#     '''


    # existed_child_nodes = set()

    # for node in nodes:
    #     childs_node = find_node_childs(node, nodes, affect_radius)

    #     if tree_type == 'TREE':
    #         for child_node in childs_node:
    #             if child_node not in existed_child_nodes:
    #                 insert_child_node(node, child_node)
    #                 existed_child_nodes.add(child_node)
    #     elif tree_type == 'DAG':
    #         for child_node in childs_node:
    #             insert_child_node(node, child_node)

# def assign_nodes_child(nodes, affect_radius, tree_type):
#     '''
#     Assign the child nodes to the nodes

#     Args:
#         nodes (list[Node]): The nodes
#         affect_radius (int): The affect radius
#         tree_type (str): The type of the tree (DAG or TREE)
#     '''

#     if tree_type not in ['DAG', 'TREE']:
#         raise ValueError('The tree type must be either "DAG" or "TREE"')

#     existed_child_nodes = set()

#     for node in nodes:
#         childs_node = find_node_childs(node, nodes, affect_radius)

#         if tree_type == 'TREE':
#             for child_node in childs_node:
#                 if child_node not in existed_child_nodes:
#                     insert_child_node(node, child_node)
#                     existed_child_nodes.add(child_node)
#         elif tree_type == 'DAG':
#             for child_node in childs_node:
#                 insert_child_node(node, child_node)

# def assign_nodes_position(nodes, topo_graph):
#     '''
#     Assign the node position

#     Args:
#         nodes (list[Node]): The nodes
#         topo_graph (list[list]): The topo graph

#     Returns:
#         topo_graph (list[list]): The topo graph
#     '''

#     unassigned_nodes = [node for node in nodes if node.coordinate == {}]
#     i = 0

#     while i < len(topo_graph) and unassigned_nodes != []:
#         for j in range(len(topo_graph[i])):
#             if topo_graph[i][j] == '-1':
#                 node = unassigned_nodes.pop(0)
#                 topo_graph[i][j] = node.name
#                 assign_coordinate(node, i, j)

#             if unassigned_nodes == []:
#                 break

#         i += 1

#     return topo_graph

# def assign_nodes_conflict(nodes):
#     '''
#     Assign the conflict nodes to the nodes

#     Args:
#         nodes (list[Node]): The nodes
#     '''

#     for node in nodes:
#         for child_node in node.childs_node:
#             insert_conflict_node(node, child_node)