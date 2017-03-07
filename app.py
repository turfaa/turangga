from flask import Flask
from flask import render_template

from userapi import userapi, showUrl
from urlapi import urlapi
from resolver import resolver
from line import line

from util import data_to_response

app = Flask(__name__)
app.register_blueprint(userapi, url_prefix = '/user')
app.register_blueprint(urlapi, url_prefix = '/url')
app.register_blueprint(resolver, url_prefix = '/s')

@app.errorhandler(404)
def error404(e):
    return data_to_response(False, {'message' : '404 Not Found'})

@app.route('/')
def index():
    return data_to_response(True, {'message' : 'Dear freenom, this is a working site'})

if __name__ == "__main__":
    app.run(port = 5000, host = '0.0.0.0', debug = 1, threaded = True)
