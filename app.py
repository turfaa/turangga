from flask import Flask

from userapi import userapi
from urlapi import urlapi
from resolver import resolver

from util import local_make_response

app = Flask(__name__)
app.register_blueprint(userapi, url_prefix = '/user')
app.register_blueprint(urlapi, url_prefix = '/url')
app.register_blueprint(resolver, url_prefix = '/s')

@app.errorhandler(404)
def error404(e):
    return local_make_response(False, {'message' : '404 Not Found'})


if __name__ == "__main__":
    app.run(port = 5000, host = '0.0.0.0', debug = 1, threaded = True)
