from flask import Blueprint
from flask import request

from dbhandler import DBHandler
from dbhandler import DBException

from util import data_to_object
from util import data_to_response

from myconfig import baseurl

userapi = Blueprint('userapi', __name__)

@userapi.route('/register', methods = ['POST'])
def register(local = False, username = None, password = None):
    if local:
        local_make_response = data_to_object
        if (username is None) | (password is None):
            return local_make_response(False, {'message' : 'Invalid data'})

    else:
        local_make_response = data_to_response

        if (not('username' in request.form)) | (not('password' in request.form)):
            return local_make_response(False, {'message' : 'Invalid data'})

        username = request.form['username']
        password = request.form['password']

    if (len(username) < 2):
        return local_make_response(False, {'message' : 'Username\'s length should be more than 2'})

    if (len(password) < 8):
        return local_make_response(False, {'message' : 'Password\'s length should be more than 7'})

    db = DBHandler()
    try:
        db.userCreate(username, password)
    except DBException as err:
        return local_make_response(False, {'message' : err.message})
    else:
        return local_make_response(True)

@userapi.route('/login', methods = ['POST'])
def login(local = False, username = None, password = None):
    if local:
        local_make_response = data_to_object

        if (username is None) | (password is None):
            return local_make_response(False, {'message' : 'Invalid data'})
    else:
        local_make_response = data_to_response

        if (not('username' in request.form)) | (not('password' in request.form)):
            return local_make_response(False, {'message' : 'Invalid data'})

        username = request.form['username']
        password = request.form['password']

    db = DBHandler()
    try:
        db.userLogin(username, password)
    except DBException as err:
        return local_make_response(False, {'message' : err.message})
    else:
        return local_make_response(True, {'token' : db.tokenNew(username)})

@userapi.route('/logout', methods = ['POST'])
def logout(local = False, token = None):
    if local:
        local_make_response = data_to_object
    else:
        local_make_response = data_to_response
        if 'token' in request.form:
            token = request.form['token']

    if not(token is None):
        db = DBHandler()
        db.userLogout(request.form['token'])

    return local_make_response(True)

@userapi.route('/changePassword', methods = ['POST'])
def changePassword(local = False, token = None, oldPassword = None, newPassword = None):
    if local:
        local_make_response = data_to_object

        if (token is None) | (oldPassword is None) | (newPassword is None):
            return local_make_response(False, {'message' : 'Invalid data'})

    else:
        local_make_response = data_to_response

        if (not('token' in request.form)) | (not('oldPassword' in request.form)) | (not('newPassword' in request.form)):
            return local_make_response(False, {'message' : 'Invalid data'})

        token = request.form['token']
        oldPassword = request.form['oldPassword']
        newPassword = request.form['newPassword']

    db = DBHandler()
    try:
        username = db.tokenLookup(token)
        db.userChangePassword(username, oldPassword, newPassword)
    except DBException as err:
        return local_make_response(False, {'message' : err.message})
    else:
        return local_make_response(True)

@userapi.route('/showurl', methods = ['POST'])
def showUrl(local = False, token = None):
    if local:
        local_make_response = data_to_object

        if token is None:
            return local_make_response(False, {'message' : 'Invalid data'})

    else:
        local_make_response = data_to_response

        if not ('token' in request.form):
            return local_make_response(False, {'message' : 'Invalid data'})

        token = request.form['token']

    db = DBHandler()
    try:
        username = db.tokenLookup(token)
        urls = db.userOwn(username)
    except DBException as err:
        return local_make_response(False, {'message' : err.message})
    else:
        urls = list(urls)

        for i in range(len(urls)):
            urls[i] = list(urls[i])
            urls[i][0] = baseurl + urls[i][0]

        return local_make_response(True, {'url' : urls})
