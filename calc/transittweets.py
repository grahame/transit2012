#!/usr/bin/env python3

import csv, sys, json, time, datetime
sys.path.append('../couchdb-python3/')
import couchdb
from string import digits, ascii_letters

if __name__ == '__main__':
    def log(s):
        print(s, file=sys.stderr)

    twitter_date_fmt = '%a %b %d %H:%M:%S +0000 %Y'
    search_date_fmt = '%a, %d %b %Y %H:%M:%S +0000'
    def datetime_strptime(s):
        try:
            return datetime.datetime.strptime(s, twitter_date_fmt)
        except ValueError:
            return datetime.datetime.strptime(s, search_date_fmt)

    def tweet_dectime(tweet):
        dt = datetime_strptime(tweet['created_at'])
        return dt.hour + dt.minute/60. + dt.second/3600.

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
    
    def embedded_time(text):
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
            yield(''.join(''.join([t for t in garbage if t in ascii_letters])))
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
                return h + m/60. + s/3600., numparts[-1]
            except ValueError:
                return None
        def getzone(s):
            t = s.strip().upper()
            if len(t) < 3:
                return None
            if t in zonedata:
                return t, zonedata[t]
        toks = text.split()
        times = [gettime(t.strip()) for t in toks]
        times = [t for t in times if t is not None]
        if len(times) == 0:
            return None, None, "no time found"
        elif len(times) > 1:
            raise Exception("found more than one time in tweet")
        else:
            time, garbage = times[0]
            possibilities = toks+[garbage]
            zones = [getzone(t) for t in possibilities]
            zones = [t for t in zones if t is not None]
            if len(zones) > 1:
                raise Exception("found more than one time zone in tweet")
            elif len(zones) == 1:
                zone_name, zone = zones[0]
                notes = "zone found: %s" % (zone_name)
            else:
                notes = "no zone, assume GMT"
                zone = 0.
            return time, zone, notes

    def contact_time(tweet):
        time, zone, notes = embedded_time(tweet['text'])
        if time is None or zone is None:
            time = tweet_dectime(tweet)
            zone = 0.
            method = "tweet_time"
        else:
            method = "embedded_time, " + notes
        return time, zone, method

    def decode_tweet(id, tweet):
        text = tweet['text']
        ctype = contact_type(text)
        lat, lng = lat_lng(tweet)
        out.writerow([id, tweet['text'], tweet_user(tweet), ctype, lat, lng] + list(contact_time(tweet)))

    with open('zones.json') as fd:
        zonedata = json.load(fd)
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
            raise
            log("can't decode tweet (id %s), exception %s" % (tweet['id'], e))

