import sys, os
import numpy, pickle
import re, nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import *
import scraper
import time as t

meta_data = {}
structure = {}
inv_index = {}

# Create an instance of the fanfiction scraper
scraper = scraper.Scraper()

# Read in the story_id numbers from a file
# These are unique identifiers we can use to get a story
ID_PATH = './sids.txt'
story_ids = []


# define a safe version of open that makes sure the file exists in the first place.
with open(ID_PATH) as f:
    for line in f:
        story_ids.append(line)

def scrape_data(list_of_story_ids):
    # Begin scraping
    total_chapters = 0
    pattern = re.compile('[\W_]+')
    stemmer = PorterStemmer()
    
    for element in list_of_story_ids:
        if total_chapters > 3000:
            break
        print 'Pulled %s chapters so far.' % total_chapters
        element = int(element)
        try:
            # 1. download the story / extract metadata
            story = scraper.scrape_story(element)

            title = story.get('title')
            author = story.get('author_id')
            author = 'u' + str(author)
            genre = story.get('genres')
            genre = ', '.join([str(x) for x in genre])
            rated = story.get('rated')
            lang = story.get('lang')
            num_words = story.get('num_words')
            num_chapt = story.get('num_chapters')
            status = story.get('status')

            if num_chapt == None:
                num_chapt = 1
            total_chapters = total_chapters + num_chapt
            
            meta_data[element] = [title, author, genre, rated, lang, num_words, num_chapt, status]
            print meta_data[element]

            # 2. handle the structure (to be used with pagerank)
            # -- stories point to authors (one to one)
            structure[element] = [author]
            # -- authors point to their stories (one to many)
            if author in structure:
                structure[author].append(element)
            else:
                structure[author] = [element]
            # -- users point to stories (element) (many to many)
            reviews = set()
            for chapter_key in story['reviews']:
                for review in story['reviews'][chapter_key]:
                    if review['user_id'] != None:
                        reviews.add(review['user_id'])
            for user in reviews:
                fixed_user = 'u' + str(user)
                if fixed_user in structure:
                    structure[fixed_user].append(element)
                else:
                    structure[fixed_user] = [element]
                
            #print structure

            # 3. handle the inverted index
            all_words = []
            for chapter in story['chapters']:
                text = story['chapters'][chapter]
                text = re.sub(pattern, ' ', text.lower())
                word_list = nltk.word_tokenize(text)
                filtered_and_stemmed_words = [stemmer.stem(word) \
                                              for word in word_list \
                                              if word not in \
                                              stopwords.words('english')]
                all_words = all_words + filtered_and_stemmed_words

                #store words references as tuples
                #inv_index[yellow] = [tuple(id,occurs), tuple(id, occurs)]
            
            current_file = str(element)
            for word in all_words:
                if word in inv_index:
                    temporary_string = inv_index[word].split()
                    temporary_string_length = len(temporary_string)
                    files_found = []
                    for i in range(0, temporary_string_length):
                        files_found.append(temporary_string[i].split(':')[0])
                        if temporary_string[i].split(':')[0] == current_file:
                            new_number = int(temporary_string[i].split(':')[1]) + 1
                            new_entry = current_file + ':' + str(new_number)
                            del temporary_string[i]
                            temporary_string.append(new_entry)
                            update = ' '.join(temporary_string)
                            inv_index[word] = update
                            break
                    if current_file not in files_found:
                        update = ' '.join(temporary_string) + ' ' + current_file + ':1'
                        inv_index[word] = update
                else:
                    new_entry = current_file + ':1 '
                    inv_index[word] = new_entry
            '''
            for word in all_words:
                if word in inv_index:
                    for tupl in inv_index[word]:
                        present = [item[0] for item in inv_index[word]]
                        if element in present:
                            for tupl in inv_index[word]:
                                ID, OCCUR = tupl
                                if ID == element:
                                    inv_index[word].remove(tuple([ID,OCCUR]))
                                    inv_index[word].append(tuple([ID,OCCUR+1]))
                        else:
                            inv_index[word].append([tuple([element, 1])])
                else:
                    inv_index[word] = [tuple([element, 1])]
                        
            #print 'inv_index has %s entries' % len(inv_index)
            '''
            print '\n\nWaiting for three seconds and updating log file...'
            with open('download-log.txt', 'a') as log:
                log.write(str(element) + '\n')
            t.sleep(3)
        except:
            print "ERROR: Could not scrape story with id=%s" % element
            print '\n\nWaiting for three seconds and updating log file...'
            with open('download-log.txt', 'a') as log:
                log.write('ERROR: Could not scrape story with id ' + str(element) + '\n')
            t.sleep(3)
        
    with open('metadata.csv', 'a') as meta:
        #header:
        meta.write('story|title|author|genre|rated|language|number_of_words|number_of_chapters|status\n')
        #everything else
        for key in meta_data:
            meta.write(str(key) + '|' + '|'.join([str(x).replace('|','') for x in meta_data[key]]) + '\n')
    with open('structure.csv', 'a') as struct:
        for key in structure:
            struct.write(str(key) + '|' + '|'.join([str(x).replace('|','') for x in structure[key]]) + '\n')
    with open('invindex.dat', 'a') as inverted_index:
        for key in inv_index:
            inverted_index.write(str(key) + '|' + '|'.join([str(x).replace('|','') for x in inv_index[key].split()]) + '\n')

if __name__ == '__main__':
    scrape_data(story_ids)
