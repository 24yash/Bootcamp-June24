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
    # READ Part
    blogs = Blog.query.all()
    # querying for all blogs present in the app
    return render_template('dashboard.html', username=session['username'], blogs = blogs)

import os

@app.route('/create_blog', methods=['GET', 'POST'])
def create_blog():

    # we want to know who is the current logged in user
    user = User.query.filter_by(username = session['username']).first()

    if request.method == 'POST':
        # get info from form provided by the user about the new blog that the user wants to create.
        new_title = request.form['title']
        new_content = request.form['content']
        image = request.files['image']

        if image: # image may not be provided by the user
            filename = image.filename

            # user provided image called as lion.png
            # os will store it as static/images/lion.png

            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        
        if(len(new_title)<1):
            flash('Title not Provided')
            return redirect(url_for('create_blog'))
        
        # create a new entry in the db. new blog is like an object of Blog class
        new_blog = Blog(title = new_title, content = new_content, image_url = filename, user_id = user.id)

        db.session.add(new_blog)
        db.session.commit()

        # change this to specific route for the blog made
        return redirect(url_for('dashboard'))
    
    return render_template('create_blog.html')

@app.route('/blog/<int:id>') # id here is the blog id of the blog that the user wants to read
def blog(id):
    particular_blog = Blog.query.get(id) 
    return render_template('blog.html', blog=particular_blog)

@app.route('/blog/edit/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    blog = Blog.query.get(id)
    if request.method == 'POST':
        # changing existing values to new values provided by the user through the form
        blog.title = request.form['title']
        blog.content = request.form['content']
        db.session.commit()
        return redirect(url_for('blog', id = blog.id))
    return render_template('edit_blog.html', blog = blog)

@app.route('/blog/delete/<int:id>', methods=['POST'])
def delete_blog(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('dashboard'))


# CRUD - Create, Read, Update and Delete 