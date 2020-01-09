import logging.config
import os

from flask import Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from api import Config
from api.database import DBConn

__all__ = ['app']

app = Flask(__name__)


@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    if os.environ.get['FLASK_ENV'] == 'development':
        return str(exception), 500
    else:
        return jsonify({'message': 'error'}), 500


try:
    config = Config()
    logging.config.dictConfig(config.Logging)
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        logging.info('Starting app')

        app.config.update(config.Flask)
        toolbar = DebugToolbarExtension(app)

        from blueprints import tables, test

        app.register_blueprint(tables)
        app.register_blueprint(test)

        DBConn()
    else:
        logging.info('Skipping reloader')

except Exception as e:
    logging.error(e)
    raise e
