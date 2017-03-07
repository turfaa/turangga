from flask import Blueprint
from flask import request

from util import data_to_response
from util import data_to_object

from dbhandler import DBHandler
from dbhandler import DBException

from myconfig import baseurl

import validators

urlapi = Blueprint('urlapi', __name__)

@urlapi.route('/create', methods = ['POST'])
def create(local = False, url = None, short = None, token = None):
    if local:
        local_make_response = data_to_object

        if url is None:
            return local_make_response(False, {'message' : 'Invalid data'})
    else:
        local_make_response = data_to_response

        if (not('url' in request.form)):
            return local_make_response(False, {'message' : 'Invalid data'})
        url = request.form['url']

        if 'short' in request.form:
            short = request.form['short']
        else:
            short = None

        if 'token' in request.form:
            token =request.form['token']

    if not(token is None):
        try:
            username = db.tokenLookup(request.form['token'])
        except DBException as err:
            return local_make_response(False, {'message' : err.message})
    else:
        username = None

    db = DBHandler()

    if not validators.url(url):
        return local_make_response(False, {'message' : 'URL is not valid.'})

    newUrl = baseurl

    try:
        newUrl += db.urlNew(url, short, username)
    except DBException as err:
        return local_make_response(False, {'message' : err.message})
    else:
        return local_make_response(True, {'url' : newUrl})

@urlapi.route('/delete', methods = ['POST'])
def delete(local = False, short = None, token = None):
    if local:
        local_make_response = data_to_object

        if (short is None) | (token is None):
            return local_make_response(False, {'message' : 'Invalid data'})
    else:
        local_make_response = data_to_response
        if ((not('short' in request.form)) | (not('token' in request.form))):
            return local_make_response(False, {'message' : 'Invalid data'})

        short = request.form['short']
        token = request.form['token']

    db = DBHandler()
    try:
        username = db.tokenLookup(token)
        db.urlDelete(username, short)
    except DBException as err:
        return local_make_response(False, {'message' : err.message})
    else:
        return local_make_response(True)
