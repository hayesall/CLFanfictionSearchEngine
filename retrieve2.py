import sys, os, math
import csv, pickle

# how to run: python retrieve2.py word1 word2 word3 ...

# ******************************************************
# *    Step 0: unit tests to ensure inputs are valid   *
# * At the top so that other imports won't interfere.  *
# ******************************************************

arg_list = [] #handle an arbitrary number of inputs
for arg in sys.argv[1:]:
    arg_list.append(arg)

def input_test():
    number_of_errors = 0
    if len(arg_list) < 1:
        print "\033[0;31m -- Error: invalid number of arguments, you need at least one word\033[0m"
        exit()
    else:
        print "\033[1;32mNumber of arguments is valid.\033[0m"
#    if os.path.isfile('docs.dat') and os.path.isfile('invindex.dat'):
    if os.path.isfile('metadata.csv') and os.path.isfile('invindex.dat'):
        print "\033[1;32mFound docs.dat and invindex.dat\033[0m"
    else:
        print "\033[0;31m -- Error: missing files, you need docs.dat and invindex.dat. Did you forget to ./buildindex.sh?\033[0m"
        number_of_errors += 1
    if number_of_errors > 0:
        print "\033[0;31mFound " + str(number_of_errors) + " errors, cannot continue.\033[m"
        exit()

input_test()

# ******************************************************
# *      Step 1: import and parse the documents        *
# *             docs.dat and invindex.dat              *
# ******************************************************

import nltk
import operator
from nltk.corpus import stopwords
from nltk.stem.porter import *

stemmer = PorterStemmer()
filtered_words = [word for word in arg_list if word not in stopwords.words('english')]
stemmed_words = [stemmer.stem(word) for word in filtered_words]
list_of_word_strings = [str(word) for word in stemmed_words]
#list_of_word_strings now contains all the words we need to query in the inverted index
#print "stemmed and filtered: " + str(list_of_word_strings)

#inverted_index_dict = {}
#with open('invindex.dat') as inverted_index:
#    inverted_index_list = inverted_index.readlines()

#for line in inverted_index_list:
#    content = line.split()
#    word = str(content[0])
#    documents_as_string = ""
#    for item in content[2:]:
#        documents_as_string = documents_as_string + str(item) + ' '
#    inverted_index_dict[word] = documents_as_string

#print len(inverted_index_dict)

#document_data_dict = {}
#with open('docs.dat') as doc_data:
#    document_data_list = doc_data.readlines()

#for line in document_data_list:
#    content = line.split()
#    key = str(content[0])
#    document_info = ""
#    for item in content[1:]:
#        document_info = document_info + str(item) + ' '
#    document_data_dict[key] = document_info

with open('invindex.dat', 'r') as input_file:
    reader = csv.reader(input_file, delimiter='|')
    inverted_index_dict = dict((rows[0], rows[1:]) for rows in reader)

# metadata_dict --> document_data_dict for consistency
with open('metadata.csv', 'r') as input_file:
    reader = csv.reader(input_file, delimiter='|')
    document_data_dict = dict((rows[0], rows[1:]) for rows in reader)

pagerank = pickle.load( open( 'pr.pickle', 'rb') )
#print pagerank

documents_explored = 0

most_dict = {}
frequency_dict = {}
for html_doc in document_data_dict.keys():
    for word in list_of_word_strings:
        if inverted_index_dict.has_key(word):
            #text_list: all of the documents that match a certain word
            text_list = inverted_index_dict[word]#.split()
            term_frequency = 0
            #total number of times a word occurs in all of the documents
            for item in text_list:
                head, sep, tail = item.partition(':')
                term_frequency += int(tail)
#            print text_list
#            print term_frequency
            for item in text_list:
                documents_explored += 1
                #head is the docID (42.html), sep is the separator (':'), tail is the term frequency (3)
                head, sep, tail = item.partition(':')
                tail = float(tail)
                if head == html_doc:
                    if most_dict.has_key(head):
                        most_dict[head] += 1
                    else:
                        most_dict[head] = 1
                    if frequency_dict.has_key(head):
                        frequency_dict[head] += (tail/term_frequency)
                    else:
                        frequency_dict[head] = (tail/term_frequency)

for item in frequency_dict:
    # adding pagerank is the same as not including pagerank
    # multiplying seems to create the largest effect
    frequency_dict[item] = frequency_dict[item] + (3 * pagerank[item])

# "selecting elements of python dictionary greater than a certain value"
stripped_most_dict = dict((k, v) for k, v in most_dict.items() if v >= int(math.ceil(len(list_of_word_strings)/2)))
sorted_frequency_dict = sorted(frequency_dict.items(), key=operator.itemgetter(1))
sorted_frequency_dict.reverse()
#print sorted_frequency_dict

fixed_list = []
current = 0
maximum = 100
for item in sorted_frequency_dict:
    if item[0] in stripped_most_dict:
        if current >= maximum:
            break
        else:
            fixed_list.append(item[0])
            current += 1

#print current
#print most_dict
#    print fixed_list
#    print len(fixed_list)
total_found = 0
print "\033[1;32m\n\nSuper-Google Results:\033[0m"
for item in fixed_list:
    final_list = document_data_dict[item]#.split()
    url_to_print = 'https://www.fanfiction.net/s/' + str(item)
    title_to_print = final_list[0]
    author_href = '<a href="' + 'https://www.fanfiction.net/u/' + str(final_list[1]).replace('u','') + '">' + 'Author</a>'
    link_href = '<h3><a href="' + url_to_print + '">' + title_to_print + '</a></h3>'
    #frequency_to_print = "{0:.3f}".format(float(frequency_dict[item]))
    frequency_to_print = str(frequency_dict[item])
    genre = final_list[2]
    rating = final_list[3]
    language = final_list[4]
    num_words = str(final_list[5])
    num_chapt = str(final_list[6])
    status = final_list[7]
    print '  ' + str(frequency_to_print) + ') ' + link_href
    '''
    print '          ' + author_href + \
        ', Genre: ' + genre + \
        ', Rated: ' + rating + \
        ', Language: ' + language + \
        ', Words: ' + num_words + \
        ', Chapters: ' + num_chapt + \
        ', Status: ' + status
    '''
    total_found += 1

print "Explored " + str(len(sorted_frequency_dict)) + " documents and found " + str(total_found) + " results."
