

from utils.PMC import PMC

def PMC_decNet(network, good_H_list):
    # Use PMC model propagation to detect nodes in H
    cur_good_list = good_H_list
    while(len(cur_good_list)):
        new_add_list = []
        for node in cur_good_list:
            #If a vertex has not been tested and is a faultless node to pass the PMC test, add it to new_add_list
            for node_id in node.neighbors[0]:
                if network.all_node[node_id].status == -1:
                    network.all_node[node_id].status = 1
                    if PMC(node, network.all_node[node_id]) == 0: #If it's not tested and it's still faultless, join it.
                        network.all_node[node_id].dec_level = 0
                        new_add_list.append(network.all_node[node_id])
                    else:
                        network.all_node[node_id].dec_level = -1
        cur_good_list = new_add_list

    return network