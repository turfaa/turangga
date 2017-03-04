import string
import random
import json
from flask import make_response

def randomString(length, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def local_make_response(status, data = None):
    r = make_response(json.dumps({'status' : status, 'data' : data}))
    r.headers['Content-Type'] = 'application/json; charset=utf-8'

    return r
