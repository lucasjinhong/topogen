class Link:
    '''
    Represent a link in the topology.
    '''
    __slots__ = ['name', 'data_rate', 'node', 'link_conflict']

    def __init__(self, name, node_up, node_down, data_rate):
        '''
        Initializes a new instance of the Link class.

        Args:
            name (str): the name of the link
            node_up (Node): the up node
            node_down (Node): the down node
            data_rate (int): the data rate of the link
        '''

        self.name = name
        self.data_rate = data_rate
        self.node = {
            'up': node_up,
            'down': node_down
        }
        self.link_conflict = []