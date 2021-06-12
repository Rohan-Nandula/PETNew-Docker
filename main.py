# main.py

from flask import Blueprint, render_template, Response
from flask_login import current_user, login_required, login_user
from . import db
import requests
import json
import random
import time
from datetime import datetime

main = Blueprint('main', __name__)
random.seed()  # Initialize the random number generator

def fetchExpenses(params):
    url="https://5996kr662d.execute-api.ap-south-1.amazonaws.com/ExpenseQA?"+params
    status = requests.request("GET",url)
    #print(status.json())
    return status.json()

# Function to add amount to wallet - AWS API Add Money to Wallet
def updatewallet(params):
    url="https://l1gdzvb6k6.execute-api.ap-south-1.amazonaws.com/addwallamount?"+params 
    status = requests.request("GET",url)
    print(status.json())
    return status.json()

# Function to add a specific expense for a user - AWS API Add Expense for a user
def setExpenses(params): 
    print(params)
    url = "https://ket0h58q15.execute-api.ap-south-1.amazonaws.com/ExpenseAPI?"+params
    status = requests.request("GET",url)
    print(status.json())
    return status.json()

# Function to fetch wallet balance - AWS API Wallet Balance
def walletBalance(params):
    url="https://ss979hyehb.execute-api.ap-south-1.amazonaws.com/WalletBalance?"+params
    status = requests.request("GET",url)
    print(status.json())
    return status.json()

@main.route('/')
@main.route('/home')
def index():
    title = "Personal Expense Tracker"
    
    return render_template("dchart.html", title = title)

@main.route('/chart-data', methods=['GET','POST'])
def dchart():
    def generate_random_data():
        while True:
            json_data = json.dumps({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    # generate_random_data() is a generator
    return Response(generate_random_data(), mimetype='text/event-stream')
	
@main.route('/profile', methods=['GET','POST'])
@login_required
def profile():
		username=current_user.name
		return render_template('profile.html', uname=username)

@main.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
		user=current_user.email
		expense_date_from=''
		expense_date_to=''
		params = "user="+user+"&expense_date_from="+expense_date_from+"&expense_date_to="+expense_date_to
		print(params)
		series_new=fetchExpenses(params)
		print(type(series_new))
		exp_dates = []
		for d in series_new:
			for k,v in d.items():
				if k == 'expense_date':
					exp_dates.append(v)
		print(exp_dates)
		home_expenses = []
		for d in series_new:
			for k,v in d.items():
				if k == 'home_expenses':
					home_expenses.append(int(v))
		print(home_expenses)
		medical_expenses = []
		for d in series_new:
			for k,v in d.items():
				if k == 'medical_expenses':
					medical_expenses.append(int(v))
		print(medical_expenses)
		vehicle_expenses = []
		for d in series_new:
			for k,v in d.items():
				if k == 'vehicle_expenses':
					vehicle_expenses.append(int(v))
		print(vehicle_expenses)
		legend1 = 'Home Expenses'
		legend2 = 'Vehicle Expenses'
		legend3 = 'Medical Expenses'		
		labels = exp_dates		
				
		return render_template('chart.html', labels=labels, legend1=legend1, legend2=legend2, legend3=legend3, home_expenses=home_expenses, vehicle_expenses= vehicle_expenses, medical_expenses=medical_expenses )

@main.route('/wallet')
def wallet():
    return render_template('updatewallet.html')
	
# Function to add amount to wallet - AWS API Add money to wallet
@main.route('/updatewalletpage', methods=['GET','POST'])
def updatewalletpage() :
    user=request.form['user']
    amount = request.form['amount']   
    params = "user="+user+"&amount="+amount
    print(params)
    data = updatewallet(params)
    print(type(data))
    
    if('errorType' in data):
        return render_template('updatewallet.html', pred="Wallet could not be updated. Your wallet balance has not changed.")
    else:
        return render_template('updatewallet.html', pred="Wallet has been updated successfully and your "+data)

@main.route('/expense')
def expense():
    return render_template('expense.html')

@main.route('/expensepage', methods=['GET','POST'])
def expensepage() :
    user=request.form['user']
    expensedate = request.form['expensedate']
    category = request.form['expensetype']
    expenseamount = request.form['expenseamount']

    # Check which type of expense is being updated
    if(category=='medical_expenses'):
        #medical_expenses = request.form['expenseamount']
        params = "user="+user+"&expense_date="+expensedate+"&medical_expenses="+expenseamount+"&home_expenses="+"0"+"&vehicle_expenses="+"0"
    elif(category=='home_expenses'):
        #home_expenses = request.form['expenseamount']
        params = "user="+user+"&expense_date="+expensedate+"&medical_expenses="+"0"+"&home_expenses="+expenseamount+"&vehicle_expenses="+"0"
    elif(category=='vehicle_expenses'):
        #vehicle_expenses = request.form['expenseamount']
        params = "user="+user+"&expense_date="+expensedate+"&medical_expenses="+"0"+"&home_expenses="+"0"+"&vehicle_expenses="+expenseamount
    else:
        render_template('expense.html', pred="Expense type is unauthorized in system.")

    response = setExpenses(params)

    json_object = json.dumps(response)
    print(json_object)
    	
    if('errorType' in json_object):
    	return render_template('expense.html', pred="Expense could not be added. Your wallet balance has not changed.")
    else:
    	return render_template('expense.html', pred=json_object)
		
# Function to fetch current wallet balance - AWS API Wallet Balance
@main.route('/wbalance')
def wbalance():
    user = current_user.email
    params="user="+user
    data=walletBalance(params)
    print(data)
    result = data.split("+")
    wbalance=result[0]
    message=result[1]
    print(wbalance,message)    
       
    if('errorType' in result):
            return render_template('login.html', pred="Wallet could not be updated. Your wallet balance has not changed.")
    else:
            return render_template('wbalance.html', pred=wbalance, message=message)