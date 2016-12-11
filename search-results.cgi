#!/usr/bin/python
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

print('Content-type: text/html\n')
print('<title>Search Results</title>')
print('<h1>Results:</h1>')
#words and genre are the two names
if not 'words1' in form:
    print('<p>words not specified</p>')
else:
    print('<p>You selected: %s</p>' % cgi.escape(form['words1'].value))
    user_words = (cgi.escape(form['words1'].value)).split()
#if not 'genre2' in form:
#    print('<p>genre not specified</p>')
#else:
#    print('<p>You selected: %s</p>' % cgi.escape(form['genre2'].value))
#    user_genre = (cgi.escape(form['genre2'].value)).split()

if len(user_words) > 0:
    filtered_words = [word for word in user_words if word.lower() not in stopwords.words('english')]
    stemmed_words = [stemmer.stem(word) for word in filtered_words]
    print('<br><hr><br><p>Stemmed/Stopped words:</p>')
    print('<p>')
    for word in stemmed_words:
        print('%s' % word)
    print('</p>')

#print ('<br><br><br><br><br><br><br>Questions? Contact Alexander L. Hayes: hayesall(at)indiana(dot)edu<br>')
#print ('<a href="https://github.iu.edu/hayesall/">GitHub</a>')

exit()
