
import random
from Node.Node import Node
from utils.reload import *


def randomGenerateNetForDecGood(self): #generate network for dec_good node only, satisfy good neiborhor
    self.faultFreeSetH = []
    self.faultFreeSetHids = []

    # print("H_Good node is forming")
    H_ids = []
    for i in range(self.H_nodes_num):
        H_ids.append(i)
    while(len(self.faultFreeSetHids) != self.H_good_num):
        i = random.randint(0, len(H_ids)-1)
        node_id = H_ids[i]
        node = Node(node_id=node_id, level=0, detection_function=True, goodN=self.g_goodN, degree=-1, graph_id=0)
        self.H.append(node)
        self.faultFreeSetH.append(node)
        self.faultFreeSetHids.append(node_id)
        H_ids.remove(node_id)
    # This cycle is: In the graph G_AN_H, all are used as faultless nodes for modeling.

    # print("Nodes in G_AN_H are being formed!")
    start_node_id = self.H_nodes_num + self.AN_nodes_num
    end_node_id = start_node_id + self.G_AN_H_nodes_num

    for index in range(start_node_id, end_node_id):
        node = Node(node_id=index, level=0, detection_function=True, goodN=self.g_goodN, degree=-1, graph_id=2)
        self.G_AN_H.append(node)
    # Among these nodes, the restriction of g_goodNeighbor is met.

    # print("Let the fautless nodes in H satisfy g_goodNeighbor")
    #We cannot achieve exactly googN for each node, and the generated result is >=, including equal to
    for node in self.faultFreeSetH:
        remain_listH = reloadListrandomGenerateNetForDecGood(self)[0]
        remain_listH.remove(node)
        while(node.g_goodN>0):
            list1size = len(remain_listH)
            nodeN = remain_listH[random.randint(0, list1size - 1)]
            while(nodeN.node_id in node.neighbors[nodeN.graph_id]):
                remain_listH.remove(nodeN)
                list1size = len(remain_listH)
                nodeN = remain_listH[random.randint(0, list1size - 1)]

            node.addNeighbor(nodeN.graph_id, nodeN.node_id)
            node.g_goodN -=1
            nodeN.addNeighbor(0, node.node_id)
            nodeN.g_goodN-=1
            self.H_all_degree -=2

    # For all nodes in G_AN_H, satisfy the restriction of g_goodNeighbor.
    # print("Making G_AN_H satisfy the restriction of g_goodNeighbor!")
    for node in self.G_AN_H:
        remain_listG_ = reloadListrandomGenerateNetForDecGood(self)[1]
        remain_listG_.remove(node)
        while(node.g_goodN>0):
            list2size = len(remain_listG_)
            nodeN = remain_listG_[random.randint(0, list2size - 1)]
            while(nodeN.node_id in node.neighbors[nodeN.graph_id]):
                remain_listG_.remove(nodeN)
                list2size = len(remain_listG_)
                nodeN = remain_listG_[random.randint(0, list2size - 1)]

            node.addNeighbor(nodeN.graph_id, nodeN.node_id)
            node.g_goodN -=1
            nodeN.addNeighbor(2, node.node_id)
            nodeN.g_goodN-=1
    # At this point, all detected nodes have completed the restriction of g_goodNeighbor.
