# Returns the parameter indicators of the network
# Return relevant data in the network, such as ϕ(G) and accuracy.



def return_para(self):
    accuracy, precision, recall = cal_apr(self)
    parameters = [  cal_score(self),
                    decConnectedSpace(self),
                    accuracy,
                    precision,
                    recall,
                    self.H_nodes_num,
                    self.H_good_num,
                    self.H_degree,
                    self.AN_nodes_num,
                    self.AN_decGood_num,
                    self.AN_degree,
                    self.G_AN_H_nodes_num,
                    self.g_goodN,
                    self.Node_level
                ]
    return parameters



def cal_score(self): # ϕ(G)
    num_node_dec = 0
    for node in self.H:
        if node.status == 1:
            num_node_dec+=1

    return (num_node_dec) / (len(self.H))

def cal_apr(self):
    TP = TN = FP = FN = 0
    for node in self.H:
        if node.status == -1:
            continue

        if node.level ==0:
            if node.dec_level == 0:
                TP+=1
            else:
                FN+=1
        else:
            if node.dec_level == 0:
                FP+=1
            else:
                TN+=1

    print("TP, TN, FP, FN: ", TP, TN, FP, FN) # FN 是0
          
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)

    return accuracy, precision, recall


def decConnectedSpace(self):
    connected_space_num = 0
    dectected_good_nodeid_list = []
    cur_list = []
    for node in self.faultFreeSetH:
        if node.node_id in dectected_good_nodeid_list:
            continue
        cur_list.append(node)
        while(len(cur_list)):
            cur_node = cur_list[0]
            cur_list.remove(cur_node)
            for nei_node_id in cur_node.neighbors[0]:
                if nei_node_id not in self.faultFreeSetHids:
                    continue
                if self.H[nei_node_id] in cur_list:
                    continue
                if nei_node_id not in dectected_good_nodeid_list:
                    cur_list.append(self.H[nei_node_id])
                    dectected_good_nodeid_list.append(nei_node_id)
        connected_space_num+=1
    return connected_space_num