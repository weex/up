#!/usr/bin/env python3

import sys, os, re, json
import socket
import requests
import apsw

from settings import *


connection = apsw.Connection(DB)

headers = {
    'User-Agent': "up API crawler/1",
}

def update_value(url, data, key):
    u = connection.cursor()
    sql = "UPDATE service SET `%s`=? where url=?" % key
    if key in data:
        value = data[key]
        u.execute(sql, (value, url))
    elif isinstance(data, list) and key in data[0]:
        value = data[0][key]
        u.execute(sql, (value, url))

def update_service(url):
    us = connection.cursor()
    res = us.execute("SELECT owner, name from service where url = ? limit 1", (url,))
    count = 0
    for row in res:
        (owner, name) = row
        count = count + 1

    # service not in our db
    if count == 0:
        return 

    if name is None or name in '':
        name = '(unknown)'

    # check if we can get a response
    answer = None
    try: 
        answer = requests.get(url)
        code = answer.status_code
    except Exception as e:
        print('%s error - %s' % (url, e)) 
        
    # service is not responding
    if answer is None:
        return

    # try to parse as json
    data = {}
    try:
        data = json.loads(answer.text)
    except:
        if code == 200:    
            print("code 200")

    ur = connection.cursor()
    ur.execute("UPDATE service SET response=?, updated=datetime('now') where url=?", (answer.text, url))

    # parse out the info file
    #if 'name' in data:
    #    name = data['name']
    #elif 'name' in data[0]:
    #    name = data[0]['name']
    #un = connection.cursor()
    #un.execute("UPDATE service SET name=? where url=?", (name, url))

    update_value(url, data, "name")
    update_value(url, data, "description")
    update_value(url, data, "owner")

    print('%s - %s' % (name, url))
    
if len(sys.argv) > 1:
    print("Trying just one.")
    url = sys.argv[1]
    update_service(url)
else:
    c = connection.cursor()
    for row in c.execute("SELECT url from service"):
        update_service(row[0])
