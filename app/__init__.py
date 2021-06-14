# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    Bootstrap(app)
    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access this page'
    login_manager.login_view = 'auth.login'

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .auser import auser as auser_blueprint
    app.register_blueprint(auser_blueprint)

    return app
