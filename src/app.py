from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

import logging.config
import os

from api.database import DBConn
from api import Config
from api.models import Models


__all__ = ['app', 'models']


app = Flask(__name__)

if not os.environ.get("WERKZEUG_RUN_MAIN"):
    config = Config()
    logging.config.dictConfig(config.Logging)
    logging.info('Starting app')

    app.config.update(config.Flask)
    DBConn()
    toolbar = DebugToolbarExtension(app)

models = Models()

from routes import *
