from flask import Blueprint
from flask import redirect

from dbhandler import DBHandler
from dbhandler import DBException

resolver = Blueprint('resolver', __name__)

@resolver.route('/')
def index():
    return "Invalid request"

@resolver.route('/<short>')
def resolve(short):
    db = DBHandler()

    try:
        redir = db.urlLookup(short)
        db.urlVisit(short)
    except DBException as err:
        return err.message
    else:
        return redirect(redir)
