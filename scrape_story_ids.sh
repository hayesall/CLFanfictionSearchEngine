#!/bin/bash
BASE="https://www.fanfiction.net/cartoon/Code-Lyoko/?&srt=1&r=103&p="
# on the date I wrote this, there were 261 pages of stories

for i in {1..261}; do
    URL=$BASE$i
    echo "$URL" && echo "$URL" >> sids.txt
    PAGE="`wget --no-check-certificate -q -O - $URL`"
    echo "$PAGE" | grep "class=stitle" | cut -c117-137 | cut -d'/' -f 3 >> sids.txt
    sleep 6
done
