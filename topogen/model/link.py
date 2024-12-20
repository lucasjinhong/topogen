from ..utils.error_handler import err_raise
from ..utils.function import dist_between_coord
from ..config.config import DATA_RATE_BPS_FORMULA


class Link:
    def __init__(self, name, src_node, dst_node, data_rate=0):
        '''
        Create a new instance of the Link class

        Args:
            name (str): the name of the link
            src_node (Node): the source node of the link
            dst_node (Node): the destination node of the link
            data_rate (int): the data rate of the link
        '''

        # error handling
        err_raise(ValueError, 'The source node and the destination node cannot be the same', src_node == dst_node)
        err_raise(ValueError, 'The source node and the destination node are not connected'
                  , src_node not in dst_node.parents and src_node not in dst_node.children)

        self.name = name
        self.data_rate_bps = data_rate
        self.src_node = src_node
        self.dst_node = dst_node

def generate_links(nodes, data_rate_equation=None):
    '''
    Generate the link

    Args:
        nodes (dict{str: Node}): the nodes

    Returns:
        links (dict{str: Link}): the links
    '''

    links = {}

    for src_node in nodes.values():
        for dst_node in src_node.children:
            dist_src_dst = dist_between_coord(src_node.coordinate, dst_node.coordinate)

            if data_rate_equation:
                data_rate = data_rate_equation(dist_src_dst)
            else:
                data_rate = DATA_RATE_BPS_FORMULA(dist_src_dst)

            link = Link((src_node.name, dst_node.name), src_node, dst_node, data_rate)
            links[link.name] = link
            src_node.links.append(link)

    return links