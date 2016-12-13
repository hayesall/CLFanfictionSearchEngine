#!/usr/bin/python
import sys, os, math
import csv, pickle
import cgi
import operator
from nltk.corpus import stopwords
from nltk.stem.porter import *

form = cgi.FieldStorage()

#genres will not be implemented in the first round, I'll save that for the stretch goals.
genres = ['Adventures', 'Angst', 'Crime', 'Drama', 'Family', 'Fantasy', 'Friendship', \
          'General', 'Horror', 'Humor', 'Hurt/Comfort', 'Mystery', 'Parody', 'Poetry', \
          'Romance', 'Sci-Fi', 'Spiritual', 'Supernatural', 'Suspense', 'Tradgedy', 'Western']
stemmer = PorterStemmer()
user_words = []
#user_genre = []

print 'Content-type: text/html\n'
print '<!DOCTYPE html>'
print '<html lang="en">'
print '<head>'
print '<meta charset="utf-8">'
print '<meta http-equiv="X-UA-Compatible" content="IE=edge">'
print '<meta name="viewport" content="width=device-width, initial-scale=1">'
print '<meta name="theme-color" content="#333399">'
print '<meta name="description" content="results for the terms you just queried">'
print '<meta name="author" content="Alexander Hayes">'
print '<title>Search Results</title>'
print '<link href="../STARAI/css/bootstrap.min.css" rel="stylesheet">'
print '<link href="../STARAI/css/ie10-viewport-bug-workaround.css" rel="stylesheet">'
print '<link href="../STARAI/css/sticky-footer-navbar.css" rel="stylesheet">'
print '<link href="../STARAI/css/starai.css" rel="stylesheet">'
print '<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->'
print '<!--[if lt IE 9]>'
print '<script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>'
print '<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>'
print '<![endif]-->'
print '<style>'
print 'a:link {'
print 'color: blue;'
print '}'
print 'a:visited {'
print 'color: red;'
print '}'
print 'body {'
#print 'background-color:#4682B4;'
print 'background-color:#EEEDEB;'
print '}'
print 'cleaned {'
print 'color:#000000;'
print 'font-size: 1.3em;'
print '}'
print 'centered {'
print 'margin: auto;'
print 'width: 50%;'
print 'padding: 15px;'
print '}'
print '</style>'
print '</head>'
print '<body>'
print '<nav class="navbar navbar-default navbar-fixed-top" style="background-color:#333399;">'
print '<div class="container">'
print '<div class="navbar-header" style="padding: 0.5em 10px; vertical-align: middle; width: 1300px; color: #EEEDEB; font-size: 1.4em;">'
print 'FanFiction | unleash your imagination'
print '</div></div></nav>'
print '<div class="container">'
print '<div class="container">'
print '<h1 style="color:#000000;">Results:</h1>'

# Here is where the bulk of the work actually happens:

if not 'words1' in form:
    print('<p class="lead cleaned" style="color:#000000;">No results.</p>')
else:
    print('<p class="lead cleaned" style="color:#000000;">Query: %s</p>' % cgi.escape(form['words1'].value))
    user_words = (cgi.escape(form['words1'].value)).split()

#if not 'genre2' in form:
#    print('<p>genre not specified</p>')
#else:
#    print('<p>You selected: %s</p>' % cgi.escape(form['genre2'].value))
#    user_genre = (cgi.escape(form['genre2'].value)).split()

print '<hr style="background-color: #000000; border-color: #000000; color: #000000;">'

if len(user_words) > 0:
    filtered_words = [word.lower() for word in user_words if word.lower() not in stopwords.words('english')]
    stemmed_words = [stemmer.stem(word) for word in filtered_words]
#    print('<p class="lead cleaned" style="color: #000000;">Stemmed/Stopped words:</p>')
#    print('<p class="lead cleaned" style="color:#000000;">')
#    for word in stemmed_words:
#        print('%s' % word)
#    print('</p>')
    list_of_word_strings = [str(word) for word in stemmed_words]
else:
    TAIL="""
    </div></div>
    <footer class="footer" style="background-color:#333399;">
    <div class="container">
    <p class="text-muted" style="color:#EEEDEB; font-size:16px;"><a href="https://github.iu.edu/hayesall/">GitHub</a></p>
    </div>
    </footer>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script src="../STARAI/js/bootstrap.min.js"></script>
    <script src="../STARAI/js/ie10-viewport-bug-workaround.js"></script>
    </body>
    </html>
    """
    print TAIL
    exit()

#inverted_index_dict = {}
#with open('invindex.dat') as inverted_index:
#    inverted_index_list = inverted_index.readlines()
with open('invindex.dat', 'r') as input_file:
    reader = csv.reader(input_file, delimiter='|')
    inverted_index_dict = dict((rows[0], rows[1:]) for rows in reader)

#metadata_dict --> document_data_dict for easy transition
with open('metadata.csv', 'r') as input_file:
    reader = csv.reader(input_file, delimiter='|')
    document_data_dict = dict((rows[0], rows[1:]) for rows in reader)

pagerank = pickle.load( open( 'pr.pickle', 'rb') )

#for line in inverted_index_list:
#    content = line.split()
#    word = str(content[0])
#    documents_as_string = ""
#    for item in content[2:]:
#        documents_as_string = documents_as_string + str(item) + ' '
#    inverted_index_dict[word] = documents_as_string

#testing
#print '<p class="lead cleaned" style="color:#000000;">%s</p>' % len(inverted_index_dict)

#metadata_dict replaces docs.dat, the number identifier is also the address on fanfiction.net/s/...
#author is at fanfiction.net/u/...

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
    #adding pagerank is the same as not including pagerank since they are so small (unless I inflated them a bit?)
    #multiplying seems to have the largest effect on the outcome
    frequency_dict[item] = frequency_dict[item] * pagerank[item]

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

#total_found = 0
#print "\033[1;32m\n\nSuper-Google Results:\033[0m"
#print '<p class="lead cleaned" style="color:#000000;">%s</p>' % str(len(fixed_list))

# Buttons: go forward/backward
if len(fixed_list) == 0:
    print '<p class="lead cleaned" style="color:#000000;">No results.</p>'
else:
    print '<center>'
    print '<div class="row">'
    print '<div class="col-sm-4"><input id="gobackward" style="padding: 2px 20px;" type="button" value="< Prev Page" onclick="prevPage();"></div>'
    print '<div class="col-sm-4"><div class="currentPage"></div></div>'
    print '<div class="col-sm-4"><input id="goforward" style="padding: 2px 20px;" type="button" value="Next Page >" onclick="nextPage();"></div>'
    print '</div></center>'
    print '<div class="container">'
    on_page = 0
    number = 0
    for item in fixed_list:
        if (number % 10) is 0:
            if on_page > 0:
                print '</div>' #close the <div class="page on_page" --> all but last
            on_page += 1
            print '<div class="page ' + str(on_page) + '">'

        final_list = document_data_dict[item]#.split()
        url_to_print = 'https://www.fanfiction.net/s/' + str(item)
        title_to_print = final_list[0]
        author_href = '<a href="' + 'https://www.fanfiction.net/u/' + str(final_list[1]).replace('u','') + '">' + 'Author</a>'
        link_href = '<h3>' + str(number+1) + '. <a href="' + url_to_print + '">' + title_to_print + '</a></h3>'
        #frequency_to_print = "{0:.3f}".format(float(frequency_dict[item]))
        #frequency_to_print = str(frequency_dict[item])
        genre = final_list[2]
        rating = final_list[3]
        language = final_list[4]
        num_words = str(final_list[5])
        num_chapt = str(final_list[6])
        status = final_list[7]
        print link_href
        print '   ' + author_href + \
            ', Genre: ' + genre + \
            ', Rated: ' + rating + \
            ', Language: ' + language + \
            ', Words: ' + num_words + \
            ', Chapters: ' + num_chapt + \
            ', Status: ' + status
        number += 1

#closing the last div and the container div from above.
if len(fixed_list) > 0:
    print '</div></div>'
    print '<br><br>'
    print '<center>'
    print '<div class="row">'
    print '<div class="col-sm-4"><input id="gobackward" style="padding: 2px 20px;" type="button" value="< Prev Page" onclick="prevPage();scrollToTop();"></div>'
    print '<div class="col-sm-4"><div class="currentPage"></div></div>'
    print '<div class="col-sm-4"><input id="goforward" style="padding: 2px 20px;" type="button" value="Next Page >" onclick="nextPage();scrollToTop();"></div>'
    print '</div></center>'

#A couple buttons at the bottom of the page as well.

print '<br><br><br>'
print '</div></div>'
print '<footer class="footer" style="background-color:#333399;">'
print '<div class="container">'
print '<p class="text-muted" style="color:#EEEDEB; font-size:16px;"><a href="https://github.iu.edu/hayesall/">GitHub</a></p>'
print '</div>'
print '</footer>'
print '<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>'

SCRIPT = """<script>
var pageIndex = 0
var pages = document.getElementsByClassName("page")
var numberOfPages = pages.length

for (i=0; i < numberOfPages; i++) {
    pages[i].style.display = "none";
}

function showPage(n) {
    if (n > numberOfPages-1) {
	pageIndex = 0
    }
    if (n < 0) {
	pageIndex = numberOfPages-1
    }
    pages[pageIndex].style.display = "block";
    $( "div.currentPage" ).replaceWith( '<div class="currentPage"><p>' + (pageIndex+1) + ' / ' + numberOfPages + '</div></p>' )
}

function nextPage() {
    pages[pageIndex].style.display = "none";
    pageIndex += 1
    showPage(pageIndex)
}

function prevPage() {
    pages[pageIndex].style.display = "none";
    pageIndex -= 1
    showPage(pageIndex)
}
showPage(pageIndex)
</script>

<script>
function scrollToTop() {
    $(window).scrollTop(0);
}
</script>
"""
print SCRIPT
#<script>window.jQuery || document.write('<script src="../STARAI/js/vendor/jquery.min.js"><\/script>')</script>
print '<script src="../STARAI/js/bootstrap.min.js"></script>'
print '<script src="../STARAI/js/ie10-viewport-bug-workaround.js"></script>'
print '</body>'
print '</html>'

exit()
