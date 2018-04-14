"""
REST API Resource Routing

http://flask-restful.readthedocs.io/en/latest/
"""
from flask import request
from random import randint
from app.api.rest.base import BaseResource, SecureResource, rest_resource

import redis,json,threading,requests

from config import REDIS_URL, REDIS_CHAN_CURR, REDIS_CHAN_GRAPH
from app.api.rest.listen import Listener

r = redis.from_url(REDIS_URL)
#client = Listener(r, [REDIS_CHAN_CURR])
#client.start()

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
    """ /resource/currencies/latest/graph """
    endpoints = ['/resource/currencies/latest/graph']

    def get(self):
        temp = r.get(REDIS_CHAN_GRAPH)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        # Prepare data. Adapted from: https://stackoverflow.com/questions/40059654/python-convert-a-bytes-array-into-json-format
        my_json = temp.decode('utf8')
        data = json.loads(my_json)
        # defaults to 200
        return data

@rest_resource
class ResourceTwo(BaseResource):
    """ /resource/currencies/list """
    endpoints = ['/resource/currencies/list']

    def get(self):
        temp = r.get(REDIS_CHAN_CURR)
        if temp is None:
            return { 'error': 'Not Found' }, 404
        # Prepare data.
        my_json = temp.decode('utf8')
        data = eval(my_json)
        return { 'currencies': data }


@rest_resource
class SecureResourceOne(SecureResource):
    """ /api/resource/two """
    endpoints = ['/resource/two/<string:resource_id>']

    def get(self, resource_id):
        return {'name': 'Resource Two', 'data': resource_id }

