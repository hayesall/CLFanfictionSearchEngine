import pickle
import networkx as nx

#I had to review how a pickle dump worked, this is a great place to get started:
#https://wiki.python.org/moin/UsingPickle

def main():
    G = nx.from_dict_of_lists(create_test_graph3())
    pr = pagerank(G)
    print pr
    #refer to note at top for pickle files
    pickle.dump( pr, open("pr.pickle", "wb") )

def run_unit_tests():
    G = nx.from_dict_of_lists(create_random_test_graph1())
    pr = pagerank(G)
    

# Useful reference for nxpagerank here:
#https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html
# The alpha score is the the random restart value, we discussed that it is typically around 0.85 in class, and sure enough
# the default value that networkx uses is also 0.85. I include it here to make it explicit.

def pagerank(graph):
    return nx.pagerank(graph, alpha=0.85)

def create_test_graph1():
    return {
        '1': ['2', '3'],
        '2': ['3'],
        '3': ['2', '4'],
        '4': ['1']
    }

def create_test_graph2():
    return {
        '1': ['4'],
        '2': ['1', '3', '4'],
        '3': ['1', '2', '4'],
        '4': []
    }

def create_test_graph3():
    return {
        '1': ['2'],
        '2': ['3'],
        '3': ['1', '4'],
        '4': ['1', '5'],
        '5': ['1', '6'],
        '6': ['1', '2']
    }

def create_test_graph4():
    return {
        '1': ['1', '2'],
        '2': ['1', '2'],
        '3': ['3', '4'],
        '4': ['3', '4']
    }

if __name__ == '__main__': main()
