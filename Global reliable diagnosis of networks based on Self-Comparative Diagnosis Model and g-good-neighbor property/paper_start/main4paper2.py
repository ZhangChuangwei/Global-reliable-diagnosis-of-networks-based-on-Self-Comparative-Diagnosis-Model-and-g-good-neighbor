#This main is designated for the paper on 'Global Reliable Diagnosis of Networks based on Self-Comparative Diagnosis Model and g-good-neighbor Property.

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import pandas as pd
from Algorithm.paper2 import paper2
from Algorithm.paper2 import p2_algo3
from network.network import Network
from utils.get_para import return_para
from utils.pmcDecNet import PMC_decNet
from utils.calSelfTec import selfTec


if __name__ == '__main__':
    
    # We adjust the parameter settings here.
    para_list = []
    # parameter settings
    cur_net = Network # the network selected
    times = 10 # The number of times the experiment is repeated for each network
    cur_algorithm = paper2   # the algorithm selected
    algo_return_H_num = 1 # The current algorithm needs to return several faultless vertices in H, because one is not enough.

    # Set the parameters for generating the network
    test_or_not = False #Set to False when running officially, and set to True to simply test whether the code runs smoothly. When set to True, the number of nodes in the network will be reduced to facilitate quick testing.


    if test_or_not:
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
        = 1000,         100,        10,         2000,           100,              50,        1000,           10,        1
        parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                          [G_AN_H_nodes], [Node_level, g_goodN]]
        para_list.append(parameters_tmp)
        # Node level is the diagnostic level defined in the paper.

    else:
        #The Subgroup 1 for ACC. We manipulate the number of fault-free vertices in H out of 1000.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     5,        4,         2000,           25,              50,        5000,           2,        2
        for i in range(15):
            parameters_tmp = [[H_nodes_num , H_good_num+i*25, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],[G_AN_H_nodes], [Node_level, g_goodN]]
        para_list.append(parameters_tmp)

        #The Subgroup 2 for ACC. We manipulate the Average Vertex Degree in H.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     5,        4,         2000,           100,              50,        5000,          2,        2
        for i in range(15):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree + i], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        #The Subgroup 3 for ACC. We manipulate the Value of the Diagnosis Level, namely, l.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     5,        4,         2000,           100,              50,        5000,           2,       2
        for i in range(15):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level+i, g_goodN]]
            para_list.append(parameters_tmp)

        #The Subgroup 4 for ACC. We manipulate the Value of g of g-good-neighbor Property.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     25,        18,         2000,           100,            50,        5000,           2,        2
        for i in range(15):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level, g_goodN+i]]
            para_list.append(parameters_tmp)

        #The Subgroup 5 for ACC. We manipulate the Value of the Diagnosis Level, namely, l, when g=1.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,      25,       18,         2000,           100,           50,           5000,           10,       1
        for i in range(10):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level+i, g_goodN]]
            para_list.append(parameters_tmp)

        #The Subgroup 1 for ϕ(G). We manipulate the number of fault-free vertices in H out of 1000.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,      25,         25,        2000,         100,            50,           5000,        10,        11
        for i in range(10):
            parameters_tmp = [[H_nodes_num, H_good_num + i * 50, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num], [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        #The Subgroup 2 for ϕ(G). We manipulate Average Vertex Degree in AN.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
             = 1000,    200,        25,          2000,          100,           20,           5000,       10,        11
        for i in range(10):
              parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num + i * 7],[G_AN_H_nodes], [Node_level, g_goodN]]
              para_list.append(parameters_tmp)

        #The Subgroup 3 for ϕ(G). We manipulate the Average Vertex Degree in H.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,      200,       13,         2000,           100,           50,             5000,     10,         11
        for i in range(10):
                 parameters_tmp = [[H_nodes_num, H_good_num, H_degree + i * 3],[AN_nodes_num, AN_decGood_num, AN_degree_num],[G_AN_H_nodes], [Node_level, g_goodN]]
                 para_list.append(parameters_tmp)

        #The Subgroup 4 for ϕ(G). We manipulate the Value of g of g-good-neighbor Property.
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,      200,        25,         2000,          100,            50,           5000,       10,        3
        for i in range(10):
              parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num], [G_AN_H_nodes], [Node_level, g_goodN + i * 2]]
              para_list.append(parameters_tmp)

    # Follow the entire process
    for parameters in para_list:
        # Each set of parameters retains a csv file
        paraList = []
        time_string = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        for i in range(times):
            print("***********************************************************************************")
            print("第"+str(i)+"次 Net")
            # start core running module!
            network = cur_net(parameters) #Generate the network. Here we only generate the network and do not detect it.
            network = selfTec(network, p2_algo3, network.Node_level)
            # good_H_list = cur_algorithm(network, algo_return_H_num, network.Node_level) #A list, the standard configuration of the general network is to use the new algorithm to detect good vertices in H, and then use PMC to internally propagate in H.
            # network = PMC_decNet(network, good_H_list) #Use the PMC model to pass through the detected vertices and detect the network inside H.
            net_para = return_para(network)#Return some detected parameters.
            paraList.append(net_para)
            # end core running module!

        names = ["H_score", "H_connected_space", "accuracy", "precision", "recall", "H_nodes", "H_goodnodes", "H_averageNodeDegree",
                "AN_nodes", "AN_goodDecGene", "AN_nodeEdge", "AN_averageDegree",
                "G_AN_H_nodes", "node_level"]
        result = pd.DataFrame(columns=names, data=paraList)
        scores = result['H_score'] #Here H_score means the ϕ(G);
        net_ave = scores.mean()
        net_max = scores.max()
        net_min = scores.min()
        net_med = scores.median()
        net_std = scores.std()

        accuracy_score = result['accuracy']
        acc_ave = accuracy_score.mean()
        acc_max = accuracy_score.max()
        acc_min = accuracy_score.min()
        acc_med = accuracy_score.median()


        H_c_s = result['H_connected_space'].mean()
        result.loc[times+1] = {'H_score': ""} #Here times+1 is the statistical data added at the end. Each parameter has one statistical data.
        result.loc[times+2] = {'H_score': "exp_times is: "+str(times)}
        result.loc[times+3] = {'H_score': "ave_score is: "+str(net_ave)}
        result.loc[times+4] = {'H_score': "max_score is: "+str(net_max)}
        result.loc[times+5] = {'H_score': "min_score is: "+str(net_min)}
        result.loc[times+6] = {'H_score': "median_score is: "+str(net_med)}
        result.loc[times+7] = {'H_score': "std_score is: "+str(net_std)} #standard deviation
        result.loc[times+8] = {'H_score': "ave_connected_space is: "+str(H_c_s)} #mean value of connectivity
        result.loc[times+9] = {'H_score': "ave_accuracy is: "+str(acc_ave)}
        result.loc[times+10] = {'H_score': "max_accuracy is: "+str(acc_max)}
        result.loc[times+11] = {'H_score': "min_accuracy is: "+str(acc_min)}
        result.loc[times+12] = {'H_score': "median_accuracy is: "+str(acc_med)}

        time_string1 = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        excel_name = time_string1+" Net Repeat "+str(times)+" times.csv"
        script_path = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_path, '..', 'experiment_result', excel_name)
        result.to_csv(save_path)
        print("%d times' average score %f: "%(times, net_ave)) 
        print("max score %f: " % (net_max))
        print("min score %f: " % (net_min))
        print("median score %f: " % (net_med))
        print("std score %f: " % (net_std))
        print("average accuracy %f: " % (acc_ave))
        print("max accuracy %f: " % (acc_max))
        print("min accuracy %f: " % (acc_min))
        print("median accuracy %f: " % (acc_med))