# moonbat webserver

from flask import Flask

from .log import RequestLogger

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'
