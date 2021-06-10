# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
import requests

auth = Blueprint('auth', __name__)

# Function to check user credentials - AWS API User Details
def check(user):
    url="https://nirmgp3j2c.execute-api.ap-south-1.amazonaws.com/fetchuser?user="+user
    status = requests.request("GET",url)
    print(status.json())
    return status.json()

# Function to register user - AWS API PutInfo
def registeruser(params):
    url = "https://nqwsosw3ag.execute-api.ap-south-1.amazonaws.com/QA?"+params
    status = requests.request("GET",url)
    print(status.json())
    return status.json()
	

@auth.route('/login', methods=['GET', 'POST'])
def login():
		if request.method == 'POST':
			email = request.form.get('email')
			password = request.form.get('password')
			if request.form.getlist('remember'):
				remember = True
			else:
				remember = False
			
			print(remember)
			user = User.query.filter_by(email=email).first()
			print(user)
			# check if the user actually exists
			# take the user-supplied password, hash it, and compare it to the hashed password in the database
			if not user or not check_password_hash(user.password, password):
				flash('Please check your login details and try again.')
				return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
			login_user(user, remember=remember) # if the above check passes, then we know the user has the right credentials
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
		params="name="+name+"&user="+user+"&phone="+phone+"&city="+city+"&occupation="+occupation+"&passw="+password
		print(params)
		#Step1 - Check User locally and persist for login process
		userlocal = User.query.filter_by(email=user).first()
		resultString = ''
		if userlocal: # if a user is found, we want to redirect back to signup page so user can try again
			resultString="User is already registered. Please login"
			return render_template('signup.html', pred=resultString)
		
		# create a new user with the form data. Hash the password so the plaintext version isn't saved.
		new_user = User(name=name, email=user, phone=phone, city=city, occupation=occupation, password=generate_password_hash(password, method='sha256'))

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
			return render_template('signup.html',pred="Either user is not available in local or could not be created in remote. Please contact admin")



			 
	    
	    
	    
	    
		
		#print(email,name)
		#local user addition
		#user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

		#if user: # if a user is found, we want to redirect back to signup page so user can try again
		#	return redirect(url_for('auth.signup'))

		# create a new user with the form data. Hash the password so the plaintext version isn't saved.
		#new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
		#print("New User being created")
		# add the new user to the database
		#db.session.add(new_user)
		#db.session.commit()
		#print("New User created")

		#return redirect(url_for('auth.login'))
	#else:
		#return render_template('signup.html')
			

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))    