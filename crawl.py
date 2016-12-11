#!/usr/bin/env python

import sys
print '\033[1;32mLaunched %s successfully.\033[0m' % (sys.argv[0])
print 'Importing packages.'
import urllib2
import os
import numpy as np #inverse poisson distribution to weight wait time between requests
import time as t
from bs4 import BeautifulSoup as bs
print '\033[1;32mImported packages successfully.\033[0m'

class InputException(Exception):
    def handle(self):
        print self.message

url_dictionary = {}

def getPageLinks(target_url, document_number):
    url = target_url
    try:
        link = urllib2.urlopen(url)
        html = link.read()
    except:
        pass

    # if everything has worked correctly, we can add the html to a file:
    write_to_document = storage_dir + str(document_number) + '.html' #pages/5.html
    with open(write_to_document,"w") as wf:
        wf.write(html)
    with open('index.dat',"a") as wf:
        wf.write(str(document_number) + " " + url + "\n")
        
    url_dictionary[url] = set()

    soup = bs(html, 'lxml')
    for tag in soup.findAll('a', href=True):
        http_absolute_link_string = str(tag['href'])[:7]
        https_absolute_link_string = str(tag['href'])[:8]
        relative_link_1_string = str(tag['href'])[:1]
        relative_link_2_string = str(tag['href'])[:2]
        pdf_file_string = str(tag['href'])[-3:]
        if http_absolute_link_string == 'http://':
            if pdf_file_string != 'pdf':
                url_dictionary[url].add(tag['href'])
        elif https_absolute_link_string == 'https://':
            #url_dictionary[url].add(tag['href'])
            continue
        elif (relative_link_1_string == '/') and (relative_link_2_string != '//'):
            #url_dictionary[url].add(url + str(tag['href']))
            continue
        elif relative_link_2_string == '//':
            #url_dictionary[url].add('http:' + tag['href'])
            continue
    with open('url-map.dat', "a") as wf:
        try:
            urls = [urls.replace(',','') for urls in url_dictionary[url]]
            mapped = ','.join(urls)
            wf.write(str(document_number) + ',' + str(url) + ',' + mapped + '\n')
        except KeyError:
            pass
 
        

def bfs(start):
    pages_explored = 0
    visited = set()
    queue = [start]
    while queue and (pages_explored < maximum_pages):

        # select an integer wait time from a poisson distribution
        # a gaussian (normal) distribution will pick numbers from a bell curve
        # a poisson distribution will more often favor numbers higher than the mean
        
        # try something like this (I did this on a RHEL 7 workstation, your mileage may vary):
        # > import numpy as np
        # > import matplotlib.pyplot as plt
        # > s = np.random.poisson(3, 100000)
        # > count, bins, ignored = plt.hist(s, 14, normed=True)
        # > plt.show()

        # https://en.wikipedia.org/wiki/Poisson_distribution
        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.poisson.html
        wait_time = (np.random.poisson(3,1))[0]
        t.sleep(wait_time)

        #pop off the first url in the queue
        url = queue.pop(0)
        if url not in visited:
            try:
                getPageLinks(url, pages_explored)
                print str(pages_explored) + "/" + str(maximum_pages) + " " + url
#                print list(url_dictionary.keys())
                visited.add(url)
                queue.extend(url_dictionary[url] - visited)
                pages_explored = pages_explored + 1
            except urllib2.URLError, e:
                visited.add(url)
                print "\033[0;31mURL Error.\033[0m"
            except UnicodeEncodeError, e:
                visited.add(url)
                print "\033[0;31mUnicode Encoding Error.\033[0m"
    return visited


def read_user_input():
    args = sys.argv
    if len(args) != 4: #sys.argv assumes item at [0] is the name of the function, e.g. crawl.py
        raise InputException(
            '\n\t\033[0;31mError on argparse, exactly three arguments are necessary.\033[0m'
            '\n\t\033[0;31mUsage: "crawl.py [seed-page] [max-pages] [sto-direc]"\033[0m'
            '\n\t\t\033[0;31mseed-page: Must be a valid url (e.g. https://www.fanfiction.net)\033[0m'
            '\n\t\t\033[0;31mmax-pages: Must be a number, hopefully less than 2000.\033[0m'
            '\n\t\t\033[0;31msto-direc: Storage directory: hopefully pages/\033[0m'
        )
    return [args[1], args[2], args[3]]
    
def sanitize_input(ls_args):
    '''
    Requires:
         a list of inputs created by read_user_input()
         e.g. (by default these will all be interpreted as strings)
         ['https://www.fanfiction.net', '2000', 'pages/']
    
    Raise an error if one occurs, otherwise continue the script.

    Returns:
         ['https://www.fanfiction.net', 2000, 'pages/']
         (notice that 2000 has been converted to an Int)
    
    '''
    if len(ls_args) != 3:
        raise InputException(
            '\n\t\033[0;31mError on argparse, exactly three arguments are necessary.\033[0m'
            '\n\t\033[0;31mUsage: "crawl.py [seed-page] [max-pages] [sto-direc]"\033[0m'
            '\n\t\t\033[0;31mseed-page: Must be a valid url (e.g. https://www.fanfiction.net)\033[0m'
            '\n\t\t\033[0;31mmax-pages: Must be a number, hopefully less than 2000.\033[0m'
            '\n\t\t\033[0;31msto-direc: Storage directory: hopefully pages/\033[0m'
        )
    url, num, drt = ls_args[0], ls_args[1], ls_args[2]
    
    # How do I check if a website exists?
    # http://stackoverflow.com/questions/16778435/python-check-if-website-exists
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        raise InputException(
            '\n\t\033[0;31mError with provided url, name or service is unknown.\033[0m'
            '\n\t\033[0;31mPerhaps try a different url or make sure spelling is correct?\033[0m'
            '\n\t\033[0;31mUsage: "crawl.py [seed-page] [max-pages] [sto-direc]"\033[0m'
        )
    except urllib2.URLError, e:
        raise InputException(
            '\n\t\033[0;31mError with provided url, could not complete the request.\033[0m'
            '\n\t\033[0;31mPerhaps try a different url or make sure spelling is correct?\033[0m'
            '\n\t\033[0;31mUsage: "crawl.py [seed-page] [max-pages] [sto-direc]"\033[0m'
        )

    # Is the provided number actually a number?
    # http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
    if not representsInt(num):
        raise InputException(
            '\n\t\033[0;31mError with provided number for [max-pages], could not convert it to an integer.\033[0m'
            '\n\t\033[0;31mPlease use a number of the form: 200. Floats will be ignored.\033[0m'
            '\n\t\033[0;31mUsage: "crawl.py [seed-page] [max-pages] [sto-direc]"\033[0m'
        )
    else:
        num = int(num)
        if not (num > 1):
            raise InputException(
                '\n\t\033[0;31mAre you just messing with me? Why would you request a negative number of pages????\033[0m'
                '\n\t\033[0;31mUsage: "crawl.py [seed-page] [max-pages] [sto-direc]"\033[0m'
            )
    
    # Did the user provide a valid path to the pages directory?
    if not os.path.isdir(drt):
        raise InputException(
            '\n\t\033[0;31mProvided directory does not exist.\033[0m'
            '\n\t\033[0;31mPlease use `mkdir pages` or something similar before running again.\033[0m'            
            '\n\t\033[0;31mUsage: "crawl.py [seed-page] [max-pages] [sto-direc]"\033[0m'
        )
    print '\033[1;32mInput passed all tests successfully.\033[0m'
    return [url, num, drt]
    

def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    

if __name__ == '__main__':
    user_input_list = read_user_input()
    user_input_list = sanitize_input(user_input_list)
    seed = user_input_list[0]
    maximum_pages = user_input_list[1]
    #one last check, if there isn't a '/' at the end, add it.
    if not user_input_list[2].endswith('/'):
        storage_dir = user_input_list[2] + '/'
    else:
        storage_dir = user_input_list[2]
    #storage_dir = user_input_list[2]
    bfs(seed)
#    for key in url_dictionary:
#        print str(key), str(url_dictionary[key]), '\n\n'
