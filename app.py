from flask import Flask
from userapi import userapi
from util import local_make_response

app = Flask(__name__)
app.register_blueprint(userapi, url_prefix = '/user')

@app.errorhandler(404)
def error404(e):
    return local_make_response(False, {'message' : '404 Not Found'})


if __name__ == "__main__":
    app.run(port = 5000, host = '0.0.0.0', debug = 1, threaded = True)
