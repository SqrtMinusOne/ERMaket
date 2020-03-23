import logging.config
import os
import traceback
from pathlib import Path
from tempfile import mkdtemp

from flask import Flask, abort, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session

from api import Config
from api.database import DBConn
from api.models import Models
from api.queries import SqlExecutor

__all__ = ['create_app']


def create_app():
    app = Flask(__name__)
    config = Config()
    Path(
        os.path.dirname(
            config.Logging['handlers']['file_handler']['filename']
        )
    ).mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(config.Logging)

    if not (not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true"):
        logging.info('Skipping reloader')
        return app

    # TODO Remove for production!
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

    login_manager = LoginManager()
    sess = Session()
    models = Models()
    User = models['system']['User']

    @login_manager.user_loader
    def get_user(login):
        with DBConn.get_session() as session:
            user = session.query(User).filter(User.login == login).first()
        return user

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return abort(401)

    @app.errorhandler(401)
    def unauthorized(err):
        return jsonify({'ok': False, 'message': 'unauthorized'}), 401

    @app.errorhandler(403)
    def forbidden(err):
        return jsonify(
            {
                'ok': False,
                'message': 'Insufficiend privilegies'
            }
        ), 403

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({'ok': False, 'message': '404 Not Found'}), 404

    @app.errorhandler(Exception)
    def internal_error(exception):
        app.logger.error(traceback.format_exc())
        response = {'ok': False, 'message': repr(exception)}
        if os.environ.get('FLASK_ENV') == 'development':
            response['traceback'] = traceback.format_exc()
        return jsonify(response), 500

    logging.info('Starting app')

    app.config.update(config.Flask)
    app.config['SESSION_FILE_DIR'] = mkdtemp()

    login_manager.init_app(app)
    sess.init_app(app)

    DBConn()
    SqlExecutor()

    from blueprints import tables, auth, transaction, sql, business_logic
    app.register_blueprint(tables)
    app.register_blueprint(auth)
    app.register_blueprint(transaction)
    app.register_blueprint(sql)
    app.register_blueprint(business_logic)
    return app
