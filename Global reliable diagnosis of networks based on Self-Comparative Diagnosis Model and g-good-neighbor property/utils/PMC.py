import random


def PMC(node1, node2):
    # The main function of this algorithm is:
    # Use node1 to detect node2, and feedback whether there is any problem with node2’s detection capability.

    if node1.returnDF():
        return 0 if node2.returnLevel() == 0 else 1
    else:
        return random.randint(0,1)
    