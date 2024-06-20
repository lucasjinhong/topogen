from model.topo import generate_topo, get_topo_info

# # not implement yet
# def __test_manual():
#     print('===========Test manual============')

#     topo_dict = {
#         'node': {},
#         'link': {}
#     }

#     donor = add_node('0', 'donor')
#     node_1 = add_node('1', 'node')

#     topo_dict['node']['0'] = donor
#     topo_dict['node']['1'] = node_1

#     donor.child_node.append(node_1)

#     link_01 = add_link(donor, node_1, 10)
#     topo_dict['link']['0-1'] = link_01

#     find_path(topo_dict['node'])
#     print(get_all_info(topo_dict['node']))    

#     print('===============End================')

# def __test_auto():
#     print('\n============Test auto=============')

#     fc = lambda x, y: randint(x * 32 * 10**6, y * 32 * 10**6)
#     data_rate_function = lambda d: round(32.4 + (31.7 * log10(d)) + (20 * log10(fc(23, 28))), 2)

#     topo_dict_tree = {
#         'node': {},
#         'link': {}
#     }

#     topo_dict_dag = {
#         'node': {},
#         'link': {}
#     }

#     topo_dict_dag, topo_graph_dag = generate_topo_automatically(distance_corresponding=lambda: 200)
#     topo_dict_tree, topo_graph_tree = generate_topo_automatically(tree_type='TREE', topo_graph=topo_graph_dag, data_rate=data_rate_function)

#     # print(topo)
#     info_dag = get_all_info(topo_dict_dag['node'], topo_graph_dag)
#     info_tree = get_all_info(topo_dict_tree['node'], topo_graph_tree)
#     print(info_dag)
#     print(info_tree)

#     print('===============End================')

if __name__ == '__main__':
    topo = generate_topo(4, 1, 3, 1)
    print(get_topo_info(topo))