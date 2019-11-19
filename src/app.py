from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

import logging.config
import os

from api.database import DBConn
from api import Config
from api.models import Models


__all__ = ['app', 'models']


app = Flask(__name__)

@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return render_template('500.html'), 500

try:
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        config = Config()
        logging.config.dictConfig(config.Logging)
        logging.info('Starting app')

        app.config.update(config.Flask)
        toolbar = DebugToolbarExtension(app)

    models = Models()

except Exception as e:
    logging.error(e)
    raise e

from routes import *
