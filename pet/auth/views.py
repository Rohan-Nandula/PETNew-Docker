#imports required
from flask import Blueprint, request, redirect, url_for, render_template, flash, abort, jsonify
from flask_login import login_required, LoginManager, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
#from .models import User
#from . import db
from pet.main import app, db
from pet.auth.__init__ import user as user
from pet.auth.models import User as User
import requests
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

# Inject login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    from pet.auser.models import User
    return User()


@login_manager.unauthorized_handler
def unauthorized_callback():
    """Unauthorized callbacks bounce to login"""
    return redirect(url_for('auth.login'))

# Function to check user credentials - AWS API User Details


def check(user):
    url = "https://nirmgp3j2c.execute-api.ap-south-1.amazonaws.com/fetchuser?user="+user
    status = requests.request("GET", url)
    print(status.json())
    return status.json()

# Function to register user - AWS API PutInfo


def registeruser(params):
    url = "https://nqwsosw3ag.execute-api.ap-south-1.amazonaws.com/QA?"+params
    status = requests.request("GET", url)
    print(status.json())
    return status.json()


@auth.route('/login', methods=['GET', 'POST'])
def login():
		if request.method == 'POST':
			email = request.form.get('user')
			password = request.form.get('password')
			if request.form.getlist('remember'):
				remember = True
			else:
				remember = False

			print(remember)
			encPassword = generate_password_hash(
			    password, method='sha256').encode("utf-8")
			user = User.query.filter_by(email=email, password=encPassword).first()
			if user is None:
				# the user was not found on the database
				return jsonify({"msg": "Bad username or password"}), 401

			# check if the user actually exists
			# take the user-supplied password, hash it, and compare it to the hashed password in the database
			print(generate_password_hash(password, method='sha256'))
			if not user or not check_password_hash(user.password, password):
				flash('Please check your login details and try again.')
				# if the user doesn't exist or password is wrong, reload the page
				return redirect(url_for('auth.login'))
			print(user)
			# create a new token with the user id inside
			#access_token = create_access_token(identity=email)
			#print("Acess token"+access_token)
			# if the above check passes, then we know the user has the right credentials
			login_user(user, remember=remember)
			return redirect(url_for('main.dashboard'))
		else:
			return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		name = request.form.get('name')
		user = request.form.get('email')
		phone = request.form.get('phone')
		city = request.form.get('city')
		occupation = request.form.get('occupation')
		password = request.form.get('password')
		tandcCheck = request.form.getlist('tandc')
		params = "name="+name+"&user="+user+"&phone="+phone + \
		    "&city="+city+"&occupation="+occupation+"&passw="+password
		print(params)
		#Step1 - Check User locally and persist for login process
		userlocal = User.query.filter_by(email=user).first()
		resultString = ''

		if userlocal:  # if a user is found, we want to redirect back to signup page so user can try again
			resultString = "User is already registered. Please login"
			return render_template('signup.html', pred=resultString)

		# create a new user with the form data. Hash the password so the plaintext version isn't saved.
		print(generate_password_hash(password, method='sha256'))
		new_user = User(name=name, email=user, phone=phone, city=city, occupation=occupation,
		                password=generate_password_hash(password, method='sha256'))

		# add the new user to the database
		db.session.add(new_user)
		db.session.commit()
		print("User registered in local Database successfully!")

		#Step2 - Check User exists remotely and create a record
		data = check(user)

		print(type(data))
		if('errorType' in data):
			return render_template('signup.html', pred="Remote registration has failed. Please contact your administrator")
		elif(not 'errorType' in data):
			remotedata = registeruser(params)
			print(str(remotedata))
			return redirect(url_for('auth.login'))
		else:
			return render_template('signup.html', pred="Either user is not available in local or could not be created in remote. Please contact admin")


@auth.route('/logout')
@login_required
def logout():
	"""Logout user and bounce to the login page"""
        logout_user()
        return redirect(url_for('main.index'))

@auth.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.filter.query(email=username, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })