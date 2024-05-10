from math import sqrt
from random import shuffle, randint

from ..utils.function import add_node, add_link

class Topo:
    def __init__(self):
        self.topo_dict = {
            'node': {},
            'link': {}
        }

        # TODO: 列出topo graph每一格的映射單位，即距離
        self.topo_graph = []

    # =======================
    # Generate method
    # =======================
    def topo_graph_generate(self, size, min_node_amount=None, max_node_amount=None, random=False, topo_graph=None):
        '''
        Generate the topo graph

        Args:
            size (int): The size of the topo graph
            random (bool): Randomly generate the topo graph | default: False
        '''
        self.topo_graph = [['0'] * size for _ in range(size)]

        # if random is True, randomly generate the IAB node
        if topo_graph:
            for i in range(size):
                for j in range(size):
                    if topo_graph[i][j] != '0':
                        self.topo_graph[i][j] = '1'

        elif random:
            if min_node_amount is None or max_node_amount is None:
                raise ValueError("min_node_amount and max_node_amount must be provided when random is True")

            # position pool stores the possible position
            position_pool = list(range(size))
            random_node_amount = randint(min_node_amount, max_node_amount)

            for row in self.topo_graph:
                shuffle(position_pool)

                # 取position_pool中前random_node_amount個的位置給IAB node
                for position in position_pool[:random_node_amount]:
                    row[position] = '1'

        # if random is False, use the information in topo_dict to generate the IAB node
        elif topo_graph:
            for i in range(size):
                for j in range(size):
                    if topo_graph[i][j] != '0':
                        self.topo_graph[i][j] = '1'
        else:
            for node in self.topo_dict['node'].values():
                x, y = node.coordinate['x'], node.coordinate['y']
                self.topo_graph[x][y] = 'd' if node.type == 'donor' else node.name

    def donor_generate(self):
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
                nodes['0'] = add_node('0', 'donor', coordinate={'x': 0, 'y': i})

        # if after midpoint has no IAB donor, create one
        if '0' not in nodes:
            nodes['0'] = add_node('0', 'donor', coordinate={'x': 0, 'y': len(self.topo_graph[0]) // 2})

    def node_generate(self, size, radiation_radius, tree_type='DAG'):
        '''
        Generate the IAB node

        Args:
            size (int): The size of the topo graph
            radiation_radius (int): The radiation radius of the IAB node
        '''

        nodes = self.topo_dict['node']
        coordinate_exist = {str(coordinate): idx for idx, coordinate in enumerate([node.coordinate for node in nodes.values()])}
        node_idx = 0

        while node_idx < len(nodes):
            node = nodes[str(node_idx)]
            child_node_coordinate = self.find_child_node_coordinate(node.coordinate, size, radiation_radius)

            for coordinate in child_node_coordinate:
                coordinate_str = str(coordinate)

                if coordinate_str in coordinate_exist:
                    if tree_type == 'DAG':
                        child_node = nodes[str(coordinate_exist[coordinate_str])]
                    elif tree_type == 'TREE':
                        continue
                else:
                    child_node_name = str(len(nodes))
                    child_node = add_node(child_node_name, 'node', coordinate={'x': coordinate[0], 'y': coordinate[1]})
                    nodes[child_node_name] = child_node
                    coordinate_exist[coordinate_str] = len(nodes) - 1

                node.child_node.append(child_node)
                node.packet['forward'][child_node.name] = []

            node_idx += 1

    def link_generate(self, data_rate_function):
        '''
        Generate the link
        '''

        for node_up in self.topo_dict['node'].values():
            for node_down in node_up.child_node:
                self.topo_dict['link'][f'{node_up.name}-{node_down.name}'] = add_link(node_up, node_down, data_rate_function)

    # TODO: use bfs graph to find the child node
    def find_child_node_coordinate(self, coordinate, size, radiation_radius):
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

        x_min, x_max = (x + 1, min(size, x + radiation_radius + 1))
        y_min, y_max = (max(0, y - radiation_radius), min(size, y + radiation_radius + 1))

        print(y_min, y, y_max)

        child_node_coordinate = [[i, j] for i in range(x_min, x_max) for j in range(y_min, y_max) if self.topo_graph[i][j] == '1']

        return child_node_coordinate

    def child_node_distance_calculate(self, node, distance_corresponding):
        '''
        Calculate the distance between the node and its child node

        Args:
            node (obj): The node object
            distance_corresponding (dict): The distance corresponding
        '''

        for child_node in node.child_node:
            distance = sqrt((node.coordinate['x'] - child_node.coordinate['x']) ** 2 + (node.coordinate['y'] - child_node.coordinate['y']) ** 2)
            node.child_node_distance[child_node.name] = distance * distance_corresponding