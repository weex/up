#!/usr/bin/env python3

import os
import json
import random
import apsw
from settings import *

from flask import Flask
from flask import request
from flask import send_from_directory

from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

connection = apsw.Connection(DB)
c = connection.cursor()


@app.route('/')
@app.route('/info')
@app.route('/help')
def home():
    '''Document the API so that other services could consume automatically.'''
    home_obj = [{"name": "up",
                 "service_version": "1",
                 "api_version": "1",
                 "description": "Provides directory services backed by a crawler. "\
                      "Download the server and crawler at https://github.com/weex/up",
                 "endpoints" : [
                                {"route": "/up",
                                 "args": None,
                                 "per-req": PRICE,
                                 "description": "Get services that have been up in the last 24 hours.",
                                 "returns": [{"name": "name",
                                              "description": "name of service"},
                                             {"name": "url",
                                              "description": "URL of crawled endpoint."}]
                                },
                                {"route": "/up-premium",
                                 "args": None,
                                 "per-req": PRICE*4,
                                 "description": "Get extended info on services that have been up "\
                                         "in the last week including time of last update.",
                                 "returns": [{"name": "name",
                                              "description": "name of service"},
                                             {"name": "url",
                                              "description": "URL of crawled endpoint."},
                                             {"name": "description",
                                              "description": "Text explaining the crawled service,"},
                                             {"name": "updated",
                                              "description": "UTC time of last successful update."}]
                                },
                                {"route": "/put",
                                 "args": [{"name": "url",
                                           "description": "URL of endpoint providing JSON-encoded data "\
                                             "about your service."}],  
                                 "per-req": PRICE,
                                 "description": "List your own endpoint here. From your 21BC, the "\
                                       "command is: 21 buy --maxprice "+ str(PRICE) +" url "\
                                       "http://10.244.34.100/put?url={your_endpoint_url}",
                                 "returns": [{"name": "result",
                                              "description": "Success or failure."},
                                             {"name": "message",
                                              "description": "(optional) Additional info."}
                                            ],
                                },
                                {"route": "/info",
                                 "args": None,
                                 "per-req": 0,
                                 "description": "This listing of endpoints provided by this server. "\
                                    "Available at / and /info."
                                }],
                }
               ]

    body = json.dumps(home_obj, indent=2)

    return (body, 200, {'Content-length': len(body),
                        'Content-type': 'application/json',
                       }
           )


@app.route('/put')
@payment.required(PRICE)
def add_listing():
    url = request.args.get('url')

    res = c.execute("SELECT url from service where url = ?", (url,))
    count = 0
    for row in res:
        count = count + 1

    if count == 0:
        c.execute("INSERT INTO service (url) VALUES (?)", (url,))
        body = json.dumps({'result': 'success'}, 
                          indent=2)
    else:
        body = json.dumps({'result': 'success',
                           'note': 'Endpoint already registered.'},
                          indent=2)

    return (body, 200, {'Content-length': len(body),
                        'Content-type': 'application/json',
                       }
           )
    
@app.route('/up')
@payment.required(PRICE)
def listing():
    services = []
    for url, owner, name in c.execute("SELECT url, owner, name from service where updated > datetime('now','-1 day')"):
        services.append({'name': name, 'url': url})

    body = json.dumps(services, indent=2) 
    code = 201
    return (body, code, {'Content-length': len(body),
                        'Content-type': 'application/json',
                        }
            )

@app.route('/up-premium')
@payment.required(PRICE*4)
def listing_premium():
    services = []
    for url, owner, name, description, updated in c.execute("SELECT url, owner, name, description, updated from service where updated > datetime('now','-7 day')"):
        services.append({'name': name, 'url': url, 'owner': owner, 'description': description, 'updated': updated})

    body = json.dumps(services, indent=2) 
    code = 201
    return (body, code, {'Content-length': len(body),
                        'Content-type': 'application/json',
                        }
            )

if __name__ == '__main__':
    if DEBUG:
       app.debug = True
    app.run(host='0.0.0.0', port=SERVER_PORT)
