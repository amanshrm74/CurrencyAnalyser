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
    """ /api/resource/one """
    endpoints = ['/resource/one']

    def get(self):
        temp = r.get(REDIS_CHAN_GRAPH)
        # Adapted from: https://stackoverflow.com/questions/40059654/python-convert-a-bytes-array-into-json-format
        my_json = temp.decode('utf8')
        # Load the JSON to a Python list, then format as JSON
        data = json.loads(my_json)
        return data

    def post(self):
        json_payload = request.json
        return {'name': 'Resource Post'}


@rest_resource
class SecureResourceOne(SecureResource):
    """ /api/resource/two """
    endpoints = ['/resource/two/<string:resource_id>']

    def get(self, resource_id):
        return {'name': 'Resource Two', 'data': resource_id }

