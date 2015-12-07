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
    '''Return service, pricing and endpoint information'''
    home_obj = [{"name": "up/1",            # service name/version
                 "pricing-type": "per-req",
                 "pricing" : [{"rpc": "up",
                               "per-req": PRICE,
                               "description": "Lists available services at time of last crawl."
                              },
                              {"rpc": "put",        # True indicates default
                               "per-req": PRICE,
                               "per-mb": 0,
                               "description": "List your own endpoint here. From your 21BC, the "\
                                       "command is: 21 buy --maxprice "+ str(PRICE) +" url "\
                                       "http://10.244.34.100/put?url={your_endpoint_url}. If you "\
                                       "a url that we already have, you'll get a note that it's "\
                                       "already registered."
                              },
                              {"rpc": "info",        # True indicates default
                               "per-req": 0,
                               "per-mb": 0,
                               "description": "This listing of endpoints provided by this server. "\
                                    "Available at / and /info."
                              },

                              # default
                              {"rpc": True,        # True indicates default
                               "per-req": 0,
                               "per-mb": 0
                              }],
                  "description": "This Up server provides directory services backed by a crawler. "\
                      "Download the client and server at https://github.com/weex/up"
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

if __name__ == '__main__':
    if DEBUG:
       app.debug = True
    app.run(host='0.0.0.0', port=SERVER_PORT)
