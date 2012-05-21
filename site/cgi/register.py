#!/usr/bin/python3

import cgi, cgitb, sys, json, re, os
sys.path.append("/home/grahame/code/undulatus/couchdb-python3")
import couchdb
import urllib.parse, urllib.request
import http.client, json

def geocode(address):
    uri = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s' % (urllib.parse.quote(address))
    req = urllib.request.Request(uri)
    with urllib.request.urlopen(req) as fd:
        resp = fd.read().decode('utf8')
    geocode = json.loads(resp)
    if 'status' not in geocode or geocode['status'] != 'OK':
        return None
    result = geocode['results'][0]
    loc = result['geometry']['location']
    return loc['lat'], loc['lng']

def register(username, location):
    if not re.match(r'^[a-zA-Z0-9_]{1,15}$', username):
        return "invalid twitter username"
    if location == "":
        return "invalid location"
    srv = couchdb.Server()
    db = srv['registrations']
    try:
        del db[username]
    except couchdb.http.ResourceNotFound:
        pass
    lat, lng = geocode(location)
    db[username] = { "location" : location, "lat" : lat, "lng" : lng }
    return "You have been registered."

def write_regos():
    tf = "/home/grahame/code/transit2012/tmp/%d.tmp" % (os.getpid())
    with open(tf, 'w') as fd:
        srv = couchdb.Server()
        db = srv['registrations']
        results = []
        for nm in db:
            doc = db[nm]
            if 'location' in doc and 'lat' in doc or 'lng' in doc:
                results.append((nm, doc['location'], doc['lat'], doc['lng']))
        json.dump(results, fd)
    os.rename(tf, "/home/grahame/code/transit2012/site/regos/regos.json")

if __name__ == '__main__':
    cgitb.enable()
    form = cgi.FieldStorage()
    if "twitter" in form and "location" in form:
        twitter = form['twitter'].value
        result = register(form['twitter'].value, form['location'].value)
    else:
        result = "invalid request, no username and/or location"
    write_regos()
    sys.stdout.write("Content-type: text/plain\r\n\r\n")
    sys.stdout.write(json.dumps({"result": result}))


