#It is specially used for self-detection type of algorithms, and calculates the corresponding simulation indicators through TP TN FP and FN


def selfTec(network, algorithm, l=7):
    '''
        Network refers to the current network.
        Algorithm refers to the algorithm to be self-tested.
    '''
    for node in network.H:
        algorithm(network, node, network.Node_level)

    return network