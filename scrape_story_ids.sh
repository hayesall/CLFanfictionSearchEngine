#!/bin/bash
BASE="https://www.fanfiction.net/cartoon/Code-Lyoko/?&srt=1&r=10&p="
# on the date I wrote this, there were 261 pages of stories
# update 12/30/2016 changing r=103 to r=10 allows scraping of stories rated M

# update 12/30/2016, 261 -> 285 to include 594 stories that are rated M
#for i in {1..261}; do
for i in {1..285}; do
    URL=$BASE$i
    echo "$URL" && echo "$URL" >> sids.txt
    PAGE="`wget --no-check-certificate -q -O - $URL`"
    echo "$PAGE" | grep "class=stitle" | cut -c117-137 | cut -d'/' -f 3 >> sids.txt
    sleep 6
done
