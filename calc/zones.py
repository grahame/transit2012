#!/usr/bin/env python3

import csv, re, json, sys

# parses table from http://en.wikipedia.org/wiki/List_of_time_zone_abbreviations

zones = {}
r = re.compile(r'^UTC(.)?((\d+(:\d+)?))?')
with open("zones.txt") as fd:
    reader = csv.reader(fd)
    for row in reader:
        if len(row) < 3: continue
        abbrev, name, tm = row
        abbrev = abbrev.strip().upper()
        if not tm.startswith('UTC'):
            raise Exception()
        grps = (r.match(tm).groups())
        num = grps[2]
        if num is None:
            utc_offset = 0
        else:
            sp = num.split(':')
            assert(len(sp) <= 2)
            utc_offset = int(sp[0]) * 60
            if len(sp) > 1:
                utc_offset += int(sp[1])
        if grps[0] and grps[0] != '+':
            utc_offset = -utc_offset
        zones[abbrev] = utc_offset
json.dump(zones, sys.stdout)
