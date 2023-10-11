import random

# 这个作为模板

from Node.Node import Node
from utils.randomGenerateNetForDecGood import randomGenerateNetForDecGood
from utils.distribute import distribute
from utils.reload import *


class Network(object):
    def __init__(self, parameters):
        self.H_p = parameters[0] # graph_id = 0 H_p means H network related parameters
        [self.H_nodes_num, self.H_good_num, self.H_degree] = self.H_p
        self.H_all_degree = self.H_degree * self.H_nodes_num
        self.AN_p = parameters[1] # graph_id = 1
        [self.AN_nodes_num, self.AN_decGood_num, self.AN_degree] = self.AN_p
        self.AN_all_degree = self.AN_degree * self.AN_nodes_num

        self.G_AN_H_p = parameters[2] # graph_id = 2
        [self.G_AN_H_nodes_num] = self.G_AN_H_p

        self.node_p = parameters[3]
        [self.Node_level, self.g_goodN] = self.node_p

        self.H = []
        self.AN = []
        self.G_AN_H = []
        self.all_net = []
        #The naming order of the nodes here is H + AN + (G-AN-H), and this order is uniform

        #The part to generate a network
        randomGenerateNetForDecGood(self) #When modeling connections between nodes, all networks are identical.
        self.randomGenerateNetOthers() #The connection between the AN network and other points is tentatively the same for every company.

        self.H.sort(key=lambda x:x.node_id)
        self.AN.sort(key=lambda x:x.node_id)
        self.G_AN_H.sort(key=lambda x:x.node_id)

        self.all_node = self.H + self.AN + self.G_AN_H
        print("Network Has Been Generated!")

    def randomGenerateNetOthers(self):
        remain_neighbor_AN_num = self.AN_all_degree #This is the total degree in the current AN.

        self.faulFreeSetAN = []
        self.faulFreeSetANids = []
        AN_ids = []

        start_node_id = self.H_nodes_num
        end_node_id = start_node_id + self.AN_nodes_num

        for index in range(start_node_id, end_node_id):
            AN_ids.append(index)


        while(len(self.faulFreeSetANids) != self.AN_decGood_num):
            i = random.randint(0, len(AN_ids)-1)
            node_id = AN_ids[i]
            node = Node(node_id=node_id, level=random.randint(1, self.Node_level), detection_function=True, goodN=0, degree=0, graph_id=1) #对它的好邻居个数没有要求
            self.AN.append(node)
            self.faulFreeSetAN.append(node)
            self.faulFreeSetANids.append(node_id)
            rangeJ = random.randint(0, len(self.G_AN_H)-1)
            node.addNeighbor(2, self.G_AN_H[rangeJ].node_id)
            self.G_AN_H[rangeJ].addNeighbor(1, i)
            AN_ids.remove(node_id)


        for node_id in AN_ids:
            node = Node(node_id = node_id, degree=0, detection_function=False, goodN=0, level=random.randint(1, self.Node_level), graph_id=1)
            self.AN.append(node)
            rangeJ = random.randint(0, len(self.G_AN_H)-1)
            node.addNeighbor(2, rangeJ)
            self.G_AN_H[rangeJ].addNeighbor(1, node_id)
        remain_neighbor_AN_num -= self.AN_nodes_num

        for index in range(self.H_nodes_num):
            if index not in self.faultFreeSetHids:
                node = Node(node_id=index, degree=-1, detection_function=False, goodN=0,
                            level=1, graph_id=0)
                self.H.append(node)

        rangeI = random.randint(0, len(self.H)-1)
        rangeJ = random.randint(0, len(self.AN) - 1)
        node = self.H[rangeI]
        node.addNeighbor(1, rangeJ)
        self.AN[rangeJ].addNeighbor(0, node.node_id)
        remain_neighbor_AN_num -= 1
        self.H_all_degree -= 1


        an_degree = distribute(self, degree_sum=remain_neighbor_AN_num, part_num=self.AN_nodes_num, covariance=remain_neighbor_AN_num/self.AN_nodes_num/5)
        for index in range(self.AN_nodes_num):
            self.AN[index].degree = an_degree[index]


        for node in self.AN:
            AN_nei_candidate_list = reloadANinnerNeighbor(self, node)
            try:
                cur_node_num = 3
                if node.degree<cur_node_num:
                    continue
                while(cur_node_num):
                    rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                    nodeN = AN_nei_candidate_list[rangeJ]

                    while((nodeN.degree == 0) or nodeN.node_id in node.neighbors[nodeN.graph_id]):# 像G_AN_H的degree都是从-1开始的, 永远不可能是0, 因为要一直减
                        AN_nei_candidate_list.remove(nodeN)
                        rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                        nodeN = AN_nei_candidate_list[rangeJ]

                    if nodeN.graph_id == 0:
                        node.addNeighbor(0, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    if nodeN.graph_id == 1:
                        node.addNeighbor(1, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    if nodeN.graph_id == 2:
                        node.addNeighbor(2, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    node.degree -=1
                    cur_node_num -=1
                    nodeN.degree-=1
            except:
                pass

        h_degree = distribute(self, degree_sum=self.H_all_degree, part_num=self.H_nodes_num, covariance=self.H_all_degree/self.H_nodes_num/5)
        for index in range(self.H_nodes_num):
            self.H[index].degree = h_degree[index]

        for node in self.H:
            H_nei_candidate_list = reloadHneighbor(self, node)
            while(node.degree>0):
                rangeJ = random.randint(0, len(H_nei_candidate_list)-1)
                nodeN = H_nei_candidate_list[rangeJ]

                while((nodeN.degree == 0) or nodeN.node_id in node.neighbors[nodeN.graph_id]):
                    H_nei_candidate_list.remove(nodeN)
                    rangeJ = random.randint(0, len(H_nei_candidate_list)-1)
                    nodeN = H_nei_candidate_list[rangeJ]

                if nodeN.graph_id == 0:
                    node.addNeighbor(0, nodeN.node_id)
                    nodeN.addNeighbor(0, node.node_id)
                if nodeN.graph_id == 1:
                    node.addNeighbor(1, nodeN.node_id)
                    nodeN.addNeighbor(0, node.node_id)
                if nodeN.graph_id == 2:
                    node.addNeighbor(2, nodeN.node_id)
                    nodeN.addNeighbor(0, node.node_id)
                node.degree -=1
                nodeN.degree-=1



        for node in self.AN:
            AN_nei_candidate_list = reloadANneighbor(self, node)
            try:
                while(node.degree):
                    rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                    nodeN = AN_nei_candidate_list[rangeJ]

                    while((nodeN.degree == 0) or nodeN.node_id in node.neighbors[nodeN.graph_id]):
                        AN_nei_candidate_list.remove(nodeN)
                        rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                        nodeN = AN_nei_candidate_list[rangeJ]

                    if nodeN.graph_id == 0:
                        node.addNeighbor(0, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    if nodeN.graph_id == 1:
                        node.addNeighbor(1, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    if nodeN.graph_id == 2:
                        node.addNeighbor(2, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    node.degree -=1
                    nodeN.degree-=1
            except:
                pass