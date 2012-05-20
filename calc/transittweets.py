#!/usr/bin/env python3

import csv, sys
sys.path.append('../../undulatus/couchdb-python3/')
import couchdb
import time
from string import digits

if __name__ == '__main__':
    def log(s):
        print(s, file=sys.stderr)

    def tweet_user(tweet):
        # cope if we've got a crappy search tweet without embedded user
        if 'user' in tweet:
            return tweet['user']['screen_name']
        else:
            return tweet['from_user']

    def contact_type(text):
        if text.find('enter') != -1:
            return 'enter'
        elif text.find('leave') != -1 or text.find('left') != -1:
            return 'left'
        else:
            raise Exception("unknown contact; `%s'" % (text))
    
    def lat_lng(tweet):
        if not "geo" in tweet:
            raise Exception("tweet is not geocoded")
        coords = tweet['geo']['coordinates']
        lat, lng = coords
        return float(lat), float(lng)
    
    def contact_time(tweet):
        def npiter(s):
            garbage = []
            r = []
            for c in s:
                if c in digits:
                    r.append(c)
                else:
                    garbage.append(c)
                    if len(r) > 0:
                        yield(''.join(r))
                        r = []
            if len(r) > 0:
                yield ''.join(r)
            yield(''.join(garbage))
        def gettime(s):
            numparts = list(npiter(s))
            if len(numparts) != 4:
                return None
            try:
                h, m, s = [int(t) for t in numparts[:3]]
                if h < 0 or h > 23:
                    return None
                if m < 0 or m > 59:
                    return None
                if s < 0 or s > 59:
                    return None
                return h, m, s
            except ValueError:
                return None
        times = [gettime(t.strip()) for t in tweet['text'].split()]
        times = [t for t in times if t is not None]
        if len(times) == 0:
            raise Exception("can't find time in tweet")
        elif len(times) > 1:
            raise Exception("found more than one time in tweet")
        else:
            return times[0]

    def decode_tweet(id, tweet):
        text = tweet['text']
        ctype = contact_type(text)
        lat, lng = lat_lng(tweet)
        h, m, s = contact_time(tweet)
        out.writerow((id, tweet_user(tweet), ctype, lat, lng, h, m, s))

    dbname, hashtag = sys.argv[1:]
    srv = couchdb.Server('http://localhost:5984/')
    db = srv[dbname]
    out = csv.writer(sys.stdout)
    for row in db.view('undulatus/byhashtag')[hashtag]:
        tweet = db[row.id]
        if 'retweeted_status' in tweet:
            log("ignored retweet (id %s)" % tweet['id'])
            continue
        try:
            decode_tweet(row.id, tweet)
        except Exception as e:
            log("can't decode tweet (id %s), exception %s" % (tweet['id'], e))

