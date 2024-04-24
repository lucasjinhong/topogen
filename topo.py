from random import randint, shuffle
from math import sqrt, ceil

__all__ = ['Topo']

'''
寫topo_graph中每一格所映射的單位
'''

class Topo:
    def __init__(self):
        self.topo_dict = {
            'node': {},
            'link': {}
        }
        self.topo_graph = {}

    # =======================
    # Adding method
    # =======================
    def add_link(self, node_up_name, node_down_name, **kwargs):
        '''
        Add link into topo

        Args:
            node_up_name (str): Node up 
            node_down_name (str): Node down

            advanced:
                data rate (int): Data rate | default: random

        Returns:
            link (obj): Link object
        '''
        arg_list = ['data_rate']

        if kwargs != {}:
            self._kwargs_arg_checker(kwargs, arg_list)
        
        if node_up_name not in self.topo_dict['node']:
            raise ValueError(f'{node_up_name} not exist')
        if node_down_name not in self.topo_dict['node']:
            raise ValueError(f'{node_down_name} not exist')
        if self.topo_dict['node'][node_down_name].type == 'donor':
            raise ValueError(f'{node_down_name} is donor, cannot be down node')

        link_name = f'{node_up_name}-{node_down_name}'
        node_up = self.topo_dict['node'][node_up_name]
        node_down = self.topo_dict['node'][node_down_name]

        if node_down not in node_up.child_node:
            node_up.child_node.append(node_down)

        link = Link()
        link.create_link(link_name, node_up, node_down, **kwargs)

        node_up.link['down'].append(link)
        node_down.link['up'].append(link)

        node_up.link_reserve_time[link] = {
            'start': 0,
            'end': 0
        }

        self.topo_dict['link'][link_name] = link

        return link

    def add_node(self, node_name, node_type, **kwargs):
        '''
        Add node into topo

        Args:
            name (str): Node name
            type (str): Node type (IAB donor or IAB node)

            advanced:
                coordinate (dict): Coordinate of the node
                {'x': int, 'y': int}

        Returns:
            node (obj): Node object
        '''
        args = ['coordinate']

        if kwargs != {}:
            self._kwargs_arg_checker(kwargs, args)

        if node_name in self.topo_dict['node']:
            raise ValueError(f'{node_name} already exist')
        if node_type not in ['donor', 'node']:
            raise ValueError(f'{node_type} is not a valid type, ex.(donor|node)')

        if 'coordinate' in kwargs:
            coordinate = kwargs.pop('coordinate')

            if 'x' and 'y' not in coordinate:
                raise ValueError('x and y is required for coordinate')
        else:
            coordinate = None

        node = Node()
        node.create_node(node_name, node_type, coordinate=coordinate)
        self.topo_dict['node'][node_name] = node

        return node

    def add_rule(self, link, conflict_link):
        '''
        Add some conflict link to the link

        Args:
            link_name (str): Link name 
            conflict_link (list): Conflict link name
        '''
        link = self.topo_dict['link'][link]

        if link not in self.topo_dict['link'].values():
            raise ValueError(f'{link.name} not exist')

        for i, l in enumerate(conflict_link):
            if l not in self.topo_dict['link'].keys():
                raise ValueError(f'{l.name} not exist')
            else:
                conflict_link[i] = self.topo_dict['link'][l]

        link.link_conflict += conflict_link

    # =======================
    # Find Path method
    # =======================
    def find_path(self):
        '''
        Find all path to node
        '''

        for node in self.topo_dict['node'].values():
            if node.type == 'donor':
                donor = node

        if donor is None:
            raise ValueError('Donor not found')

        path_to_node = donor.path_to_node

        # using stack
        traversed_node_stack = [donor]


        # use DFS to find the path to node
        while traversed_node_stack:
            node = traversed_node_stack.pop()

            for node_down in node.child_node:
                if node_down not in path_to_node:
                    path_to_node[node_down] = []

                if node == donor:
                    path_to_node[node_down].append([donor, node_down])
                else:
                    for path in path_to_node[node]:
                        if path + [node_down] not in path_to_node[node_down]:
                            path_to_node[node_down].append(path + [node_down])

                traversed_node_stack.append(node_down)

    # =======================
    # Random generate method
    # =======================
    def random_generate(self, size=4, radiation_radius=2):
        '''
        Randomly generate the topo graph

        Args:
            size (int): The size of the topo graph | default: 4 | min: 4
            radiation_radius (int): The radiation radius of the IAB node | default: ceil(sqrt(size))
        '''

        assert size >= 4, 'Size must be greater than 4'
        assert radiation_radius >= 1, 'Radiation radius must be greater than 1'

        self._topo_graph_generate(size, random=True)    # random generate topo graph

        self._donor_generate()                          # generate IAB donor
        self._node_generate(size, radiation_radius)     # generate IAB node
        self._topo_graph_generate(size)

        self._link_generate()                # generate link
        self._initialize_half_duplex_rule()  # initialize half duplex rule
        self.find_path()                     # generate path to node

    # =======================
    # Generate method
    # =======================
    def _topo_graph_generate(self, size, random=False):
        '''
        Generate the topo graph

        Args:
            size (int): The size of the topo graph
            random (bool): Randomly generate the topo graph | default: False
        '''
        self.topo_graph = {}

        for i in range(size):
            self.topo_graph[i] = [0] * size

        # if random is True, randomly generate the IAB node
        if random:
            # position pool stores the possible position
            position_pool = [i for i in range(size)]
            min_node_amount = ceil(sqrt(size))
            max_node_amount = size // 2

            random_node_amount = randint(min_node_amount, max_node_amount)

            for row in self.topo_graph.values():
                shuffle(position_pool)

                # 取position_pool中前random_node_amount個的位置給IAB node
                for position in position_pool[:random_node_amount]:
                    row[position] = 1

        # if random is False, use the information in topo_dict to generate the IAB node
        else:
            for node in self.topo_dict['node'].values():
                self.topo_graph[node.coordinate['x']][node.coordinate['y']] = 1

    def _donor_generate(self):
        '''
        Generate the IAB donor
        '''

        nodes = self.topo_dict['node']
        left = len(self.topo_graph[0]) // 4 * 1
        right = len(self.topo_graph[0]) // 4 * 3

        # generate IAB donor, from the midpoint to the end
        for i in range(left, right):
            if self.topo_graph[0][i] == 1 and '0' in nodes:
                self.topo_graph[0][i] = 0

            elif self.topo_graph[0][i] == 1 and '0' not in nodes:
                self.add_node('0', 'donor', coordinate={'x': 0, 'y': i})

        # if after midpoint has no IAB donor, create one
        if '0' not in nodes:
            self.add_node('0', 'donor', coordinate={'x': 0, 'y': len(self.topo_graph[0]) // 2})

    def _node_generate(self, size, radiation_radius):
        '''
        Generate the IAB node

        Args:
            size (int): The size of the topo graph
            radiation_radius (int): The radiation radius of the IAB node
        '''

        nodes = self.topo_dict['node']
        coordinate_exist = []
        node_idx = 0

        while node_idx < len(nodes):
            node = nodes[str(node_idx)]
            coordinate = node.coordinate

            # check the child node coordinate
            child_node_coordinate = self._find_child_node_coordinate(coordinate, size, radiation_radius)

            for coordinate in child_node_coordinate:
                if coordinate in coordinate_exist:
                    coordinate_idx = coordinate_exist.index(coordinate) + 1
                    child_node_name = nodes[str(coordinate_idx)]
                else:
                    child_node_name = str(len(nodes))
                    child_node = self.add_node(child_node_name, 'node', coordinate={'x': coordinate[0], 'y': coordinate[1]})
                    
                    coordinate_exist.append(coordinate)

                node.child_node.append(child_node)

            node_idx += 1

    def _link_generate(self):
        '''
        Generate the link
        '''

        node_list = self.topo_dict['node']

        for node_up in node_list.values():
            node_downs = node_up.child_node

            for node_down in node_downs:
                self.add_link(node_up.name, node_down.name)

    def _find_child_node_coordinate(self, coordinate, size, radiation_radius):
        '''
        Find the child node coordinate

        Args:
            coordinate (dict): Coordinate of the node
            size (int): The size of the topo graph
            radiation_radius (int): The radiation radius of the IAB node

        Returns:
            child_node_coordinate (list): The child node coordinate
        '''

        x = coordinate.get('x')
        y = coordinate.get('y')

        x_min, x_max = (x + 1, min(size, x + radiation_radius))
        y_min, y_max = (max(0, y - (radiation_radius // 2)), min(size, y + (radiation_radius // 2) + 1))
        child_node_coordinate = []

        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if self.topo_graph[i][j] == 1:
                    child_node_coordinate.append([i, j])

        return child_node_coordinate

    def _initialize_half_duplex_rule(self):
        '''
        Auto Initialize the half duplex rule to the topo
        '''

        nodes = self.topo_dict['node'].values()

        for node in nodes:
            links = node.link['down'] + node.link['up']

            # check if link is conflict with other link
            for link in links:
                link_conflict = [l.name for l in links if l != link]
                self.add_rule(link.name, link_conflict)

        return

    # =======================
    # Function
    # =======================
    def _kwargs_arg_checker(self, kwargs, arg_list):
        '''
        Check if arg is in kwargs

        Args:
            kwargs (dict): The kwargs
            arg_list (list): The arg list
        '''

        for arg in arg_list:
            if arg not in kwargs:
                raise ValueError(f'{arg} is required')

    def __str__(self) -> str:
        info = ''

        info += '---------------TOPO---------------\n\n'
        nodes = self.topo_dict['node'].values()

        for node in nodes:
            info += f'Node: {node.name}\n'
            node = self.topo_dict['node'][node.name]

            for link in node.link['down']:
                reserve_time_start = node.link_reserve_time[link]['start']
                reserve_time_end = node.link_reserve_time[link]['end']

                info += f'  Link: {link.name}' + \
                        f' (Data Rate: {link.data_rate}' + \
                        f', Link Conflict: {[l.name for l in link.link_conflict]}' + \
                        f', Reservation Time: [{reserve_time_start}:{reserve_time_end}])\n'

        info += '\n---------------PATH---------------\n\n'

        for node in self.topo_dict['node'].values():
            if node.type == 'donor':
                donor = node

        for link, paths in donor.path_to_node.items():
            path = []

            for p in paths:
                path.append([n.name for n in p])

            info += f'link: {link.name} (Path: {path})\n'

        info += '\n----------------------------------\n'

        return info

class Link:
    def __init__(self):
        self.name = None
        self.data_rate = 0
        self.node = {
            'up': None,
            'down': None
        }
        self.link_conflict = []

    def create_link(self, name, node_up, node_down, data_rate=None):
        '''
        insert the link information

        Args:
            up_node (Node): the up node
            down_node (Node): the down node
            
            advanced:
                data rate (int): Data rate | default: random
        '''

        self.node['up'] = node_up
        self.node['down'] = node_down
        self.name = name

        if data_rate is not None:
            self.data_rate = data_rate
        else:
            # 之後引入data rate的計算方式
            self.data_rate = randint(5, 10)

class Node:
    def __init__(self):
        self.name = None
        self.type = None
        self.child_node = []
        self.link = {
            'up': [],
            'down': []
        }
        self.link_reserve_time = {}
        # {
        #     'link_name': {
        #         'start': 0,
        #         'end': 0
        #     },
        #     ...
        # }
        self.packet = {
            'forward': [],
            'received': []
        }

    def create_node(self, name, type_, **kwargs):
        '''
        insert the node information

        Args:
            type (str): the type of the node
        '''
        if 'coordinate' in kwargs:
            self.coordinate = kwargs.pop('coordinate')

        self.type = type_
        self.name = name

        if type_ == 'donor':
            self.path_to_node = {}

def __test_manual():
    topo = Topo()

    # add node
    topo.add_node('0', 'donor')
    topo.add_node('1', 'node')
    topo.add_node('2', 'node')
    topo.add_node('3', 'node')
    topo.add_node('4', 'node')

    # add link
    topo.add_link('0', '1')
    topo.add_link('1', '2')
    topo.add_link('2', '3')
    topo.add_link('3', '4')

    # add link error
    try:
        topo.add_link('4', '0')
    except ValueError as e:
        print('\n--------Test add link error-------\n')
        print(f'Error: {e}\n')

    # add rule
    topo.add_rule('0-1', ['1-2'])
    topo.add_rule('1-2', ['0-1', '2-3'])
    topo.add_rule('2-3', ['1-2', '3-4'])
    topo.add_rule('3-4', ['2-3'])

    # find path
    topo.find_path()

    # print(topo)
    print(topo)

def __test_auto():
    topo = Topo()
    topo.random_generate()

    for x in topo.topo_graph.values():
        print(x)
    print()

    # print(topo)
    print(topo)

if __name__ == '__main__':
    __test_manual()
    __test_auto()