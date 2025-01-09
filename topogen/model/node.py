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

        self.forward_packets = []           # the packets to be forwarded
        self.received_packets = []          # the packets received

        # distributed implementation
        self.node_to_dst = {}               # the next node to the destination ex. {node3: [node1, node2]}
        self.received_info = {}             # the received information ex. {'t': {Node: {info}})
        self.send_info = []                 # the information to be sent to neighbour node
        self.forward_info = []              # the information to be forwarded to another node

def setup_conflict_nodes(nodes):
    '''
    Setup the conflict links

    Args:
        nodes (dict{str: Node}): The nodes

    Returns:
        None
    '''

    for node in nodes.values():
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
                coord = (i, j)

                if graph[i][j] == 1 and dist_between_coord(node.coordinate, coord) <= max_dist_to_connect_nodes:
                    if coord not in existed_coordinate:
                        child_node = Node(str(len(nodes)), 'node')
                        child_node.coordinate = coord
                        existed_coordinate.append(coord)

                        nodes[child_node.name] = child_node
                        queue.append(child_node)

                    node.children.append(child_node)
                    child_node.parents.append(node)

    return nodes

def find_node_to_dst_by_graph(nodes, graph):
    '''
    Find the node to the destination

    Args:
        nodes (dict[str:Node]): The nodes
        graph (dict[str:list[Node]]): The graph

    Returns:
        None
    '''

    for i in range(len(graph) - 2, -1, -1):
        for j in range(len(graph[i])):
            if graph[i][j] == '0':
                continue

            node = nodes[graph[i][j]]

            for child in node.children:
                node.node_to_dst[child] = [child]

                for descendant in child.node_to_dst.keys():
                    node.node_to_dst.setdefault(descendant, []).append(child)