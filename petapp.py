# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
load_dotenv()
#print(os.environ)


def main():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    # database name
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    app.config['MAX_CONTENT_LENGTH'] = os.environ.get("MAX_CONTENT_LENGTH")
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = os.environ.get('JWT_BLACKLIST_ENABLED')
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = os.environ.get('JWT_BLACKLIST_TOKEN_CHECKS')
    print(app.config['SECRET_KEY'])

    from .main import main
    
    from .auth import auth

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # JwtManager object
    jwt = JWTManager(app)
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
	app = main()
	print("Value in built variable name is:  ",__name__)
	app.run(host='0.0.0.0')
