import random

# node1 sends diagnostic information to node2 (equivalent to giving node2 its own data and letting node2 measure its own results), and node2 sends its own diagnostic results to node1.


def MLEC(node1, node2, Node_level=7):
    if node1.returnDF():
        return node2.returnLevel()
    else:
        return random.randint(0, Node_level)

