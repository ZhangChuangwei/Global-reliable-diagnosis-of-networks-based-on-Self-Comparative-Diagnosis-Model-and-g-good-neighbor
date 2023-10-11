# The function of this function is to find a good vertex u in H and use this good one to detect and propagate the PMC model to diagnose.

from utils.PMC import PMC

def detectH(self, u):

    self.H_good_numNodeList = [u]
    # self.H_good_numNodeList.append(u)
    u.status = 1

    #Two indicators can be displayed, precision and accuracy

    while(len(self.H_good_numNodeList)):#When no new good vertices are added to the set, it means that the detection is completed; breadth first algorithm
        self.H_new_goodNodeList = [] #The collection of good points detected in this round
        for node in self.H_good_numNodeList:
            for node_id in node.neighbors[0]:
                if self.H[node_id].status == -1:
                    self.H[node_id].status = 1
                    if PMC(node, self.H[node_id]) == 0: #If it is not detected and it is still good, add it; PMC here is that if there is a problem with the node, it will return an incorrect result.
                        self.H_new_goodNodeList.append(self.H[node_id])
        self.H_good_numNodeList = self.H_new_goodNodeList
