
import os.path
from flask import Flask, abort, jsonify, request, make_response, render_template, redirect, url_for
from jinja2 import Template, Environment, FileSystemLoader
from flask_sqlalchemy import SQLAlchemy

import os
import pet.config as config

def create_app_and_db():
    """Create application and database"""
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(config.DevelopmentConfig)
    # Database
    db = SQLAlchemy(app)
    return app, db

# Bootstrap.
app, db = create_app_and_db()

# # Temporary - this will be made better.
# if not os.path.isfile("/tmp/db_created"):
#     from pet.auth.models import User

#     db.create_all()

#     admin = User()
#     admin.username = 'admin'
#     admin.email = 'admin@example.com'
#     admin.password_hash = None
#     admin.login_token = 'abba'

#     print admin.get_one_time_login_url()

#     db.session.add(admin)
#     db.session.commit()

#     file = open('/tmp/db_created', 'w+')


@app.route('/', methods=["GET"])
def index():
    """Index bounces to user.user_login when anonymous or present a 404 message"""
    from flask_login import current_user
    if not current_user.is_authenticated:
        return redirect(url_for('user.user_login'))
    return abort(404, 'Successfully logged in -- start creating!')

# Register blueprints
from pet import auth, auser
#app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(auth,__name__, template_folder='templates')
app.register_blueprint(auser,__name__, template_folder='templates')

if __name__ == '__main__':
    app.run()
