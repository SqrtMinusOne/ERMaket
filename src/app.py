import logging.config
import os

from flask import Flask, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager

from api import Config
from api.database import DBConn
from models import User

__all__ = ['app']

app = Flask(__name__)
login_manager = LoginManager()


@login_manager.user_loader
def get_user(login):
    with DBConn.get_session() as session:
        user = session.query(User).filter(User.login == login).first()
    return user


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return jsonify({'message': 'unauthorized'})


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
        login_manager.init_app(app)
        DBConn()

        from blueprints import tables, test, auth
        app.register_blueprint(tables)
        app.register_blueprint(test)
        app.register_blueprint(auth)
    else:
        logging.info('Skipping reloader')

except Exception as e:
    logging.error(e)
    raise e
