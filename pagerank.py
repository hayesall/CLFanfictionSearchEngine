import sys, os
import csv
import pickle
import networkx as nx
import operator

# This is meant to be imported into another function
# from pagerank import find_pagerank

#I had to review how a pickle dump worked, this is a great place to get started:
#https://wiki.python.org/moin/UsingPickle

class InputException(Exception):
    def handle(self):
        print self.message

def main():
    if not run_unit_tests():
        raise InputException(
            '\n\t\033[0;31mError on unit tests, refer to failed test cases above.\033[0m'
        )
    input_file = read_user_input()
    G = import_data(input_file)
    pr = find_pagerank(G)
    print '\033[1;32mWriting results to pr.pickle.\033[0m'
    pickle.dump( pr, open("pr.pickle", "wb") )
'''
    FILE = sys.argv[1]
    print FILE
    G = import_data(FILE)
    pr = find_pagerank(G)

    sorted_pr = sorted(pr.items(), key=operator.itemgetter(1), reverse=True)
'''
    #print sorted_pr

def read_user_input():
    args = sys.argv
    if len(args) != 2:
        raise InputException(
            '\n\t\033[0;31mError on argparse, exactly one file should be specified.\033[0m'
            '\n\t\033[0;31mMost likely a "structure.csv" file.\033[0m'
            '\n\t\033[0;31mUsage: "python pagerank.py [file]"\033[0m'
        )
    return args[1]

def import_data(file_to_read):
    print '\033[1;32mImporting dictionary graph from %s\033[0m' % file_to_read
    if not os.path.isfile(file_to_read):
        raise InputException(
            '\n\t\033[0;31mError on file import, could not find the file.\033[0m'
            '\n\t\033[0;31mMost likely a "structure.csv" file.\033[0m'
            '\n\t\033[0;31mUsage: "python pagerank.py [file]"\033[0m'            
        )
    try:
        with open(file_to_read, 'r') as input_file:
            reader = csv.reader(input_file, delimiter='|')
            G = dict((rows[0],rows[1:]) for rows in reader)
        return G
    except:
        raise InputException(
            '\n\t\033[0;31mError on file import, could not open provided file.\033[0m'
            '\n\t\033[0;31mAre you sure you imported a structure.csv with "|" as delimiters?\033[0m'
            '\n\t\033[0;31mUsage: "python pagerank.py [file]"\033[0m'
        )

def run_unit_tests():
    pr = find_pagerank(create_test_graph(1))
    test1 = (pr == {'1': 0.29521306459338925,
                    '3': 0.29521306459338925,
                    '2': 0.20478693540661067,
                    '4': 0.20478693540661067})
    pr = find_pagerank(create_test_graph(2))
    test2 = (pr == {'1': 0.25,
                    '3': 0.25,
                    '2': 0.25,
                    '4': 0.25})
    pr = find_pagerank(create_test_graph(3))
    test3 = (pr == {'1': 0.24025949489415346,
                    '3': 0.1519481010211692,
                    '2': 0.1519481010211692,
                    '5': 0.1519481010211692,
                    '4': 0.1519481010211692,
                    '6': 0.1519481010211692})
    pr = find_pagerank(create_test_graph(4))
    test4 = (pr == {'1': 0.25, '3': 0.25, '2': 0.25, '4': 0.25})
    if test1 and test2 and test3 and test4:
        return True
    else:
        tests = [test1, test2, test3, test4]
        for test in range(len(tests)):
            if not tests[test]:
                print '\033[0;31mFailed test: %i, expected pagerank value does not match.\033[0m' % (test + 1)
        return False
    
# Useful reference for nxpagerank here:
#https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html
# The alpha score is the the random restart value, we discussed that it is typically around 0.85 in class, and sure enough
# the default value that networkx uses is also 0.85. I include it here to make it explicit.

def find_pagerank(graph):
    # takes a graph in the form of a python dictionary (refer to the test graphs below)
    G = nx.from_dict_of_lists(graph)
    return nx.pagerank(G, alpha=0.85)

def create_test_graph(n):
    test_graphs = {
        1: { '1': ['2', '3'], '2': ['3'], '3': ['2', '4'], '4': ['1']},
        2: { '1': ['4'], '2': ['1', '3', '4'], '3': ['1', '2', '4'], '4': []},
        3: { '1': ['2'], '2': ['3'], '3': ['1', '4'], '4': ['1', '5'], '5': ['1', '6'], '6': ['1', '2']},
        4: { '1': ['1', '2'], '2': ['1', '2'], '3': ['3', '4'], '4': ['3', '4']},
        5: { '1': ['2'], '2': ['1'], '3': ['2'], '4': ['2', '7'], '5': ['2', '7'],
             '6': ['7'], '7': ['5'], '8': ['7', '9'], '9': ['10'], '10': ['9'], '11': ['9']}}
    if n in test_graphs.keys():
        return test_graphs[n]
    else:
        raise InputException(
            '\n\t\033[0;31mcreate_test_graph index out of range, choose 1..5\033[0m'
        )

if __name__ == '__main__': main()
