# u tests itself and has result rr(uu).
# u is a vertex in H.

# Regarding l in the algorithm, l means that if the two test results are completely consistent, it is level l. The situation from 1 to l depends on the situation. The more different the results, the lower the score;
import random

from Node import Node
from utils.MLEC import MLEC


def self_comparative_diagnosis(self, u, l=10):#The incoming u will be fed back to see if u is a faultless vertex.
    # Corresponding to Algorithm 3 in the paper

    Nad_list = find_Nad(self, u, l)
    if len(Nad_list) == 0:
        return False

    if len(Nad_list) >1:
        return Nad_2(self, u, Nad_list, l)
    else:
        return Nad_1(self, u, Nad_list, l)


def return_l(node1_level, node2_level, l):
    return l - abs(node1_level - node2_level)


def find_Nad(self, u, l=10) -> list:
    Nad_list=[]

    for nei_list in u.neighbors:
        for node_id in nei_list:
            node = self.all_node[node_id]
            node1_level = MLEC(u, u)
            node2_level = MLEC(node, u) # What is returned is the result of node measuring u.
            if return_l(node1_level=node1_level, node2_level=node2_level, l=l) == l:
                Nad_list.append(node)

    return Nad_list


def Nad_1(self, u, Nad_list, l=10) -> bool: #Returns whether the u node is faultless or faulty, True means faultless
    y1 = Nad_list[0] #len(Nad_list) == 1
    
    unode1_level = MLEC(u, y1)
    unode2_level = MLEC(y1, y1)   

    if not return_l(node1_level=unode1_level, node2_level=unode2_level, l=l) == l: #We require SE(rr(y 1y 1), rr(y 1u)) == l
        return False  

    zi_list = []
    for nei_list in y1.neighbors:
        for node_id in nei_list:
            node = self.all_node[node_id]
            if node is u:
                continue
            node1_level = MLEC(y1, y1)
            node2_level = MLEC(node, y1) 
            if return_l(node1_level=node1_level, node2_level=node2_level, l=l) == l:
                zi_list.append(node)            

    if len(zi_list) == 0: #Here is to verify the following content in algorithm:SE(rr(y1 y1), rr(y1 zi)) == l for at least one i
        return False

    z_id = random.randint(0, len(zi_list)-1)
    z = zi_list[z_id]
    znode1_level = MLEC(z, z)
    znode2_level = MLEC(y1, z) 
    
    if return_l(node1_level=znode1_level, node2_level=znode2_level, l=l) == l:
        return True
    else:
        return False


def Nad_2(self, u, Nad_list, l=10) -> bool:

    for node in Nad_list:
        node1_level = MLEC(node, node)
        node2_level = MLEC(u, node)
        if return_l(node1_level=node1_level, node2_level=node2_level, l=l) < l:
            return False# out of range 1
    
    return True
#
