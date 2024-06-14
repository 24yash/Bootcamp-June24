#  routes will be present
from flask import Flask, render_template, redirect
# render template returning html files as response

from .models import *
#  to import everything we specify '*'

from flask import current_app as app
#  as is 'alias' 

from flask import session, request, flash, url_for

@app.route('/')
def index():
    return render_template('home.html')

# signup, login, logout
# dashboard 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['username']
        user = User.query.filter_by(username=new_username).first()
        if user:
            flash('Username is already taken! Please signup with some other user name.')
            return redirect(url_for('signup'))
        
        # if statement to handle logic with password if len(password) < 8: flash('Password should be greater than 8 chars')
        # if it does not match the conditions then you can flash the user that password does not meet the conditions

        new_user = User(username = new_username, password = request.form['password'])

        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username
        # to maintain the identity of the current logged in user at the server.

        return redirect(url_for('dashboard'))
    
    return render_template('signup.html')

@app.route('/adminsignup', methods=['GET', 'POST'])
def adminsignup():
    if request.method == 'POST':
        new_username = request.form['username']
        user = Admin.query.filter_by(username=new_username).first()
        if user:
            flash('Username is already taken! Please signup with some other user name.')
            return redirect(url_for('signup'))
        
        # if statement to handle logic with password if len(password) < 8: flash('Password should be greater than 8 chars')
        # if it does not match the conditions then you can flash the user that password does not meet the conditions

        new_user = Admin(username = new_username, password = request.form['password'])

        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username
        # to maintain the identity of the current logged in user at the server.

        return redirect(url_for('admindashboard'))
    
    return render_template('adminsignup.html')

@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard():
    if 'username' not in session:
        return redirect(url_for('adminsignup'))
    return render_template('admindashboard.html', username=session['username'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        client_username = request.form['username']
        user = User.query.filter_by(username=client_username).first() # query the db for the user with the username provided by the client.
        if user and user.password == request.form['password']: # checking if user exists and if password provided by the client is same as the password stored for the user in the db.
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))
        
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])
