
import random
from utils.MLEC import MLEC


def paper2(network, algo_return_H_num, l): 
    cur_return_H_num = 0
    good_H_list = []

    for node in network.H:
        if p2_algo3(network, node, l):
            good_H_list.append(node)
            cur_return_H_num += 1
            if cur_return_H_num >= algo_return_H_num:
                break

    return good_H_list


def p2_algo3(network, node, l):

    Nad = Ndad = 0
    S = []
    if len(node.neighbors[0]) < network.g_goodN: #Because the faultless neighbor of vertices in H can only be in H
        node.status = 1
        node.dec_level = -1
        return False
    
    uu = MLEC(node, node)
    nei_list = node.neighbors[0] + node.neighbors[1]
    for nei_node_id in nei_list:
        u_nei = MLEC(node, network.all_node[nei_node_id])
        if cal_SE(node, uu, u_nei, l) == l:
            # It means there is no problem with the detection.
            Nad += 1
            S.append(network.all_node[nei_node_id])

    if Nad < network.g_goodN:
        node.status = 1
        node.dec_level = -1
        if node.level == 0:
            print("Nad < g_goodN")
        return False
    
    for nei_node in S:
        nei_nei = MLEC(nei_node, nei_node)
        nei_u = MLEC(nei_node, node)
        mid_res = cal_SE(node, nei_nei, nei_u, l)
        if  mid_res < l:
            Ndad += 1

    if Ndad ==0:
        node.status = 1
        node.dec_level = 0
        return True
    else:
        node.status = 1
        node.dec_level = -1
        return False


def cal_SE(node, level1, level2, l):
    # Calculate the similarity of the returned results.
    # The node here is w.

    # If node is a faulty vertex, then cal_SE randomly returns 1~l

    if node.level != 0:
        return random.randint(1, l)
        # If the vertex is faulty, it will be returned randomly.
    
    if level1 == level2:
        return l
    else:
        return l - level2
