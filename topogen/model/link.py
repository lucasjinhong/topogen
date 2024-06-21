class Link:
    def __init__(self, name, src_node, dst_node, data_rate=0):
        '''
        Create a new instance of the Link class

        Args:
            name (str): the name of the link
            src_node (Node): the source node of the link
            dst_node (Node): the destination node of the link
            rate (int): the data rate of the link
        '''

        if src_node == dst_node:
            raise ValueError('The source node and the destination node cannot be the same')
        elif src_node not in dst_node.parents_node or dst_node not in src_node.childs_node:
            raise ValueError('The source node and the destination node are not connected')

        self.name = name
        self.data_rate = data_rate
        self.node = {
            'src': src_node,
            'dst': dst_node
        }

def generate_link(nodes):
    '''
    Generate the link

    Args:
        nodes (list[Node]): The nodes
    '''

    links = []

    for src_node in nodes:
        for dst_node in src_node.childs_node:
            link = Link((src_node.name, dst_node.name), src_node, dst_node)
            links.append(link)

    return links

def assign_data_rate(link, data_rate):
    '''
    Assign the data rate to the link

    Args:
        link (Link): the link
        data_rate (int|function): the data rate
    '''

    link.data_rate = data_rate