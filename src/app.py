from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from api.database import DBConn
from api import Config


__all__ = ['app']


config = Config()

app = Flask(__name__)
app.config.update(config.Flask)
DBConn()
toolbar = DebugToolbarExtension(app)

from routes import *
