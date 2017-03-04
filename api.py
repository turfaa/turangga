from flask import Blueprint
from dbhandler import DBHandler
from util import local_make_response

userapi = Blueprint('userapi', __name__)

@api.route('/register', methods = ['POST'])
