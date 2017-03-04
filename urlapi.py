from flask import Blueprint
from flask import request
from util import local_make_response
from dbhandler import DBHandler
from dbhandler import DBException
from myconfig import baseurl
import validators

urlapi = Blueprint('urlapi', __name__)

@urlapi.route('/create', methods = ['POST'])
def create():
    if (not('url' in request.form)):
        return local_make_response(False, {'message' : 'Invalid data'})

    db = DBHandler()

    url = request.form['url']

    if not validators.url(url):
        return local_make_response(False, {'message' : 'URL is not valid.'})

    if 'short' in request.form:
        short = request.form['short']
    else:
        short = None

    if 'token' in request.form:
        try:
            username = db.tokenLookup(request.form['token'])
        except DBException as err:
            return local_make_response(False, {'message' : err.message})
    else:
        username = None

    newUrl = baseurl

    try:
        newUrl += db.urlNew(url, short, username)
    except DBException as err:
        return local_make_response(False, {'message' : err.message})
    else:
        return local_make_response(True, {'url' : newUrl})

@urlapi.route('/delete', methods = ['POST'])
def delete():
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
