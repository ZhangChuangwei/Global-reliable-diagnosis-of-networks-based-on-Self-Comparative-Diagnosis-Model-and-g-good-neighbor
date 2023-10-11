
#The main function of this function is to re-update neighbor nodes.

def reloadListrandomGenerateNetForDecGood(self):
    remain_listH = []
    remain_listG = []
    for node in self.faultFreeSetH:
        remain_listH.append(node)
    for node in self.G_AN_H:
        remain_listG.append(node)
    return [remain_listH, remain_listG]

def reloadANneighbor(self, cur_node):
    AN_nei_candidate_list = []
    for node in self.AN:
        AN_nei_candidate_list.append(node)
    AN_nei_candidate_list.remove(cur_node)
    #        for node in self.H:
    #            AN_nei_candidate_list.append(node)
    for node in self.G_AN_H:
        AN_nei_candidate_list.append(node)
    return AN_nei_candidate_list

def reloadANinnerNeighbor(self, cur_node):
    AN_nei_candidate_list = []
    for node in self.AN:
        AN_nei_candidate_list.append(node)
    AN_nei_candidate_list.remove(cur_node)

    return AN_nei_candidate_list

def reloadHneighbor(self, cur_node):
    H_nei_candidate_list = []
    for node in self.H:
        H_nei_candidate_list.append(node)
    H_nei_candidate_list.remove(cur_node)
    for node in self.AN:
        H_nei_candidate_list.append(node)
    return H_nei_candidate_list