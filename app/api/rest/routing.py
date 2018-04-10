"""
REST API Resource Routing

http://flask-restful.readthedocs.io/en/latest/
"""

import time
from flask import request
from random import randint
from app.api.rest.base import BaseResource, SecureResource, rest_resource

import redis
import json
import threading
import requests

from time import sleep

REDIS_URL = "redis://localhost:6379" 
REDIS_CHAN = "test"

class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        print("Item recived: " + str(item['data']))

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == b'KILL':
                self.pubsub.unsubscribe()
                print(self, "unsubsribed")
                break
            else:
                self.work(item)
            sleep(1)

r = redis.from_url(REDIS_URL)
client = Listener(r, [REDIS_CHAN])
client.start()

""" 
TODO: stream route here 
ref: https://stephennewey.com/realtime-websites-with-flask/
"""

"""
Why Server-Sent Event(SEE) Stream?
Websockets(WSs) are often favoured over SEEs as they provide a protocol surpassing that of SEEs. 
WSs provide bi-directional, full-duplex communication between the server and client.
However, this is only significant when two way communication is required.
For data that does not need to be sent from the client, traditional HTTP SEEs, that do not implement full-duplex communication and the subsequent new WS servers to handle this connection, are ideal.
Also, SSEs have a number of functionalities that WSs lack, such as automatic reconnection.
ref: https://www.html5rocks.com/en/tutorials/eventsource/basics/
"""
@rest_resource
class ResourceOne(BaseResource):
    """ /api/resource/one """
    endpoints = ['/resource/one']

    def get(self):
        time.sleep(1)
        res = {
            'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            'datasets': 
            [{
                'label': 'EURO',
                'backgroundColor': 'rgba(255, 0, 0, 0.5)',
                'data': [randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100)]
            },
            {
                'label': 'BITCOIN',
                'backgroundColor': 'rgba(169,169,169, 0.5)',
                'data': [randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 100)]
            }]
        }
        return res

    def post(self):
        json_payload = request.json
        return {'name': 'Resource Post'}


@rest_resource
class SecureResourceOne(SecureResource):
    """ /api/resource/two """
    endpoints = ['/resource/two/<string:resource_id>']

    def get(self, resource_id):
        time.sleep(1)
        return {'name': 'Resource Two', 'data': resource_id}

