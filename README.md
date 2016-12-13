### i427 - Search Informatics - Final Project

Alexander L. Hayes - [FanFiction Search Engine](cgi.soic.indiana.edu/~hayesall/engine/index.html)

---

##### Table of Contents:

  1. [Overview](#overview)
  2. [Conditions](#conditions)
  3. [Background](#background)
  4. [Reviews](#reviews)

---

##### Overview:

For the uninitiated, [FanFiction.Net](https://www.fanfiction.net/) has been around since 1998 and is the largest online repository of fanfics‒works of fiction written by the fans of existing stories‒films, books, tv shows, and video games. This search engine is my attempt at organizing [Code Lyoko](https://en.wikipedia.org/wiki/Code_Lyoko) fanfiction: the stories based on a French animated series I watched when I was younger. This particular community holds a special meaning to me since I read quite a bit between fourth and fifth grade. "Social media" wasn't a term I (or likely the public conciousness) was familiar with in 2004, but this online community of fan-writers was my first dive into the domain.

To paraphrase Professor Nick Mount, humans are art animals‒we seek to find meaning where there may otherwise be none, whether we can find it in myths, stories, or the reassembled shards of broken glass. Code Lyoko ran in the United States for four seasons between April 2004 and May 2007, but fans continue telling stories when the original creators leave. Human culture constantly evolves, being reformed each generation, shaped by the collective experiences of those who preceded. What untold stories has time forgotten? Which gods were born with the people who worshipped them and died when the last forgot them? What pieces of our language, culture, and identify as a species are founded in legends that no one remembers by ancestors that are now nameless?

> For the generation growing up now, the Internet is their window on the world. They take it for granted. It’s only us, who have seen it take shape, and are aware of all the ways it could have been different, who understand that it's fragile, contingent. The coming years will decide to what extent the Internet be a medium for consumption, to what extent it will lift people up, and to what extent it will become a tool of social control.

Maciej Cegłowski gave a great talk called ["Deep Fried Data"](http://idlewords.com/talks/deep_fried_data.htm) about machine learning, data collection, archiving the internet, and his fears that the web will become less free. Needless to say, I highly recommend it. FanFiction is not without opponents, plenty of authors see characters and stories as their own, and perhaps rightfully so. I hope this can be a useful tool to community members, I myself have never written a fanfic, but I hope in my own small way I can contribute to its existence and perhaps its preservation.

---

##### Conditions:

Refer to FanFiction.Net's ["Terms of Service"](https://www.fanfiction.net/tos/) for full details.

> E. You agree not to use or launch any automated system, including without limitation, "robots," "spiders," or "offline readers," that accesses the Website in a manner that sends more request messages to the FanFiction.Net servers in a given period of time than a human can reasonably produce in the same period by using a conventional on-line web browser. Notwithstanding the foregoing, FanFiction.Net grants the operators of public search engines permission to use spiders to copy materials from the site for the sole purpose of and solely to the extent necessary for creating publicly available searchable indices of the materials, but not caches or archives of such materials. FanFiction.Net reserves the right to revoke these exceptions either generally or in specific cases. You agree not to collect or harvest any personally identifiable information, including account names, from the Website, nor to use the communication systems provided by the Website (e.g. comments, email) for any commercial solicitation purposes. You agree not to solicit, for commercial purposes, any users of the Website with respect to their User Submissions.

---

##### Background

There exist several implementations for searching the content. I will provide a brief overview of each here with some discussion on their strengths and weaknesses.

1. [Built-in Search](https://www.fanfiction.net/search.php) on FanFiction.net includes these options: (implemented in Php)
  * Category: (example: Books >> Harry Potter)
  * Story, Writer, Forum, or Community.
  * Titles, Summaries, or both.
  * Crossovers, exclude crossovers, or any.
  * Sort by: relevance, update date, or publication date.
  * Results can then be narrowed by word count.

  Most of the time this could be enough.

2. [Dark Lord Potter's Advanced Search](http://scryer.darklordpotter.net/) has more powerful options: (implemented in Rails)
  * Search from 48 fandoms (Star Trek, Doctor Who, Babylon 5, Harry Potter, Buffy the Vampire Slayer)
  * Include results from 679 crossovers (Example: Star Trek in the Warcraft Universe)
  * Search by Title, Author, or Summary Keywords
  * Maximum of two required categories (Adventure, Angst, Supernatural, Romance)
  * Include/Exclude other categories
  * Narrow Search to stories focusing on specific characters from the fandoms
  * Include/Exclude Age Rating (K, K+, T, M)
  * Wordcount minimum, maximum.
  * Chapter minimum, maximum.
  * Sort by: Updated, Published, Wordcount, Chapters, Reviews, Favorites, Follows, "DLP Review Score," "Popular & Recent," "Long & Recent"
  * Descending/Ascending order
  
  Initially this appears to be a step in the right direction since it has a longer list of features. But the further you look into it, the more you realize it leaves a lot to be desired. The list of features is longer, but in reality there isn't much you can find with this search engine that you cannot find with FanFiction.Net's built-in implementation.

3. [Alexander's Code Lyoko Search Engine](http://cgi.soic.indiana.edu/~hayesall/engine/index.html): (implemented in Python and a bit of Bash)
  * Specific to one fandom (Code Lyoko)
  * Search results are sorted by document relavence and pagerank

  There are some major features that still need to be added to compete with the existing engines, but trading breadth for depth gives a huge bonus: searching the contents of an entire document rather than summary or title.


Imagine for a moment that you want all of Code Lyoko stories containing a reference to "Twitter." With the crawler rate I set, I was able to explore 328 stories (this doesn't sound very large, but required around 6000 requests to explore each chapter and review section). The crawler scraped backward through time: starting from the present and ending on October 2, 2015.

From these 328 documents published over the course of a year, seven results contain references to Twitter, while the [top result](https://www.fanfiction.net/s/12035101) has an underlying cyber-bullying theme. If you use the built-in search tool on FanFiction.Net, the [only result that comes up](https://www.fanfiction.net/s/8429561/1/Tweethearts).

For the purpose of this example, I will not consider Dark Lord Potter's search engine since it does not include Code Lyoko.

##### Reviews: