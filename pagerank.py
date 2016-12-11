import pickle
import networkx as nx

# This is meant to be imported into another function
# from pagerank import find_pagerank

#I had to review how a pickle dump worked, this is a great place to get started:
#https://wiki.python.org/moin/UsingPickle

def main():
    run_unit_tests()
    #G = nx.from_dict_of_lists(create_test_graph4())
    #pr = find_pagerank(G)
    #print pr
    #refer to note at top for pickle files
    #pickle.dump( pr, open("pr.pickle", "wb") )

def run_unit_tests():
    #G = nx.from_dict_of_lists(create_test_graph1())
    #pr = find_pagerank(G)
    pr = find_pagerank(create_test_graph1())
    test1 = (pr == {'1': 0.29521306459338925,
                    '3': 0.29521306459338925,
                    '2': 0.20478693540661067,
                    '4': 0.20478693540661067})
    #G = nx.from_dict_of_lists(create_test_graph2())
    #pr = find_pagerank(G)
    pr = find_pagerank(create_test_graph2())
    test2 = (pr == {'1': 0.25,
                    '3': 0.25,
                    '2': 0.25,
                    '4': 0.25})
    #G = nx.from_dict_of_lists(create_test_graph3())
    #pr = find_pagerank(G)
    pr = find_pagerank(create_test_graph3())
    test3 = (pr == {'1': 0.24025949489415346,
                    '3': 0.1519481010211692,
                    '2': 0.1519481010211692,
                    '5': 0.1519481010211692,
                    '4': 0.1519481010211692,
                    '6': 0.1519481010211692})
    #G = nx.from_dict_of_lists(create_test_graph4())
    #pr = find_pagerank(G)
    pr = find_pagerank(create_test_graph4())
    test4 = (pr == {'1': 0.25, '3': 0.25, '2': 0.25, '4': 0.25})
    if test1 and test2 and test3 and test4:
        print 'All tests passed successfully!'
    else:
        tests = [test1, test2, test3, test4]
        for test in range(len(tests)):
            if not tests[test]:
                print 'Failed test: %i' % (test + 1)
    
# Useful reference for nxpagerank here:
#https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html
# The alpha score is the the random restart value, we discussed that it is typically around 0.85 in class, and sure enough
# the default value that networkx uses is also 0.85. I include it here to make it explicit.

def find_pagerank(graph):
#    import networkx as nx
    # takes a graph in the form of a python dictionary (refer to the test graphs below)
    G = nx.from_dict_of_lists(graph)
    return nx.pagerank(G, alpha=0.85)

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
