class Node:
    '''
    Represent a node in the topology.
    '''

    def __init__(self, name, type_, coordinate):
        '''
        insert the node information

        Args:
            name (str): the name of the node
            type_ (str): the type of the node
            coordinate (dict): the coordinate of the node
        '''

        self.name = name
        self.type = type_
        self.coordinate = coordinate

        self.child_node = []                # child nodes of the node
        self.child_node_distance = {}       # distance to the child node
        self.link = {
            'up': [],
            'down': []
        }
        self.link_reserve_time = {}
        self.packet = {
            'forward': {},
            'received': []
        }

        if type_ == 'donor':
            self.path_to_node = {}