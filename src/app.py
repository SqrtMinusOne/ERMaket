import logging.config
import os
from pathlib import Path
from tempfile import mkdtemp

from flask import Flask, abort, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session

from api import Config
from api.database import DBConn
from api.models import Models

__all__ = ['create_app']


def create_app():
    app = Flask(__name__)
    # TODO Remove for production!
    CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
    config = Config()
    Path(
        os.path.dirname(
            config.Logging['handlers']['file_handler']['filename']
        )
    ).mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(config.Logging)

    login_manager = LoginManager()
    sess = Session()
    models = Models(system_only=True)
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

    @app.errorhandler(500)
    def internal_error(exception):
        app.logger.error(exception)
        if os.environ.get('FLASK_ENV') == 'development':
            return jsonify({'ok': True, 'message': str(exception)}), 500
        else:
            return jsonify({'ok': True, 'message': 'error'}), 500

    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        logging.info('Starting app')

        app.config.update(config.Flask)
        app.config['SESSION_FILE_DIR'] = mkdtemp()

        login_manager.init_app(app)
        sess.init_app(app)

        DBConn()

        from blueprints import tables, auth
        app.register_blueprint(tables)
        app.register_blueprint(auth)
    else:
        logging.info('Skipping reloader')
    return app
