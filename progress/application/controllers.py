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
    if 'username' in session:
        return redirect(url_for('dashboard'))
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

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = request.form['search_query']
    blogs = Blog.query.filter((Blog.title.like(f'%{search_query}%')) | (Blog.content.like(f'%{search_query}%'))).all()
    # list of blogs filtered based on user's search query on the column title
    return render_template('search_result.html', username=session['username'], blogs = blogs) 

@app.route('/user_search', methods=['GET', 'POST'])
def user_search():
    search_query = request.form['search_query']
    users = User.query.filter(User.username.like(f'%{search_query}%')).all()
    # list of users filtered based on user's search query on the column username
    blogs = []
    return render_template('dashboard.html', username=session['username'], blogs = blogs, users=users) 


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
    current_user = User.query.filter_by(username=session['username']).first()
    print(current_user.has_liked(particular_blog))
    count = (len(particular_blog.likers))
    return render_template('blog.html', blog=particular_blog, current_user=current_user, count = count)

# like_blog route and unlike_blog route here
@app.route('/blog/<int:id>/like', methods=['POST'])
def like_blog(id):
    blog = Blog.query.get(id)
    current_user = User.query.filter_by(username=session['username']).first()
    current_user.like(blog)
    return redirect(url_for('blog', id=id))

@app.route('/blog/<int:id>/unlike', methods=['POST'])
def unlike_blog(id):
    blog = Blog.query.get(id)
    current_user = User.query.filter_by(username=session['username']).first()
    current_user.unlike(blog)
    return redirect(url_for('blog', id=id))

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

# route for user profile
@app.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()

    blogs = Blog.query.filter_by(user_id=user.id).all()
    number_of_blogs = len(blogs)

    # i will check if this page is being viewed by current logged in user or not and send appropriate data according to that
    # so this means that follower/following list to be shown only to the user who is viewing their own profiles
    if session['username']==username:
        # This is the case when the current user is viewing their own profile
        return render_template('user_profile.html', user = user, blogs=blogs, number_of_blogs=number_of_blogs, followers=user.followers(), following=user.following(), is_self=True)
        # is_self is a variable with value true when the current user is viewing their own profile
    else:
        # This is the case when the current user is viewing someone else profile
        current_user = User.query.filter_by(username = session['username']).first()
        # current_user and user are different. current_user is the logged in user and 'user' is the user whose profile is being viewed
        is_following = current_user.is_following(user)
        number_followers = len(user.followers())
        number_following = len(user.following())
        return render_template('user_profile.html', user = user, blogs=blogs, number_of_blogs=number_of_blogs, followers=user.followers(), following=user.following(), is_self=False, is_following=is_following, number_followers=number_followers, number_following=number_following)

@app.route('/follow/<username>')
def follow_route(username):
    user_to_follow = User.query.filter_by(username=username).first()
    current_user = User.query.filter_by(username = session['username']).first()
    current_user.follow(user_to_follow)
    return redirect(url_for('user_profile', username=username))


@app.route('/unfollow/<username>')
def unfollow_route(username):
    user_to_unfollow = User.query.filter_by(username=username).first()
    current_user = User.query.filter_by(username = session['username']).first()
    current_user.unfollow(user_to_unfollow)
    return redirect(url_for('user_profile', username=username))

import pandas as pd 
import matplotlib.pyplot as plt

@app.route('/chart')
def chart():
    # chart route for blog engagement analysis

    # x axis -> blog title
    # y axis -> number of likes (engagement)

    blog_likes = []
    for blog in Blog.query.all():
        blog_likes.append((blog.title, len(blog.likers)))

    # blog_likes list contain tuples in the format (title, number of likes)

    df = pd.DataFrame(blog_likes, columns = ['Blog', 'Likes'])

    plt.figure(figsize=(8,5))
    # x-axis values, y-axis values
    plt.bar(df['Blog'], df['Likes'])

    plt.title('Blog Engagement Analysis!')
    # x label y label
    plt.xlabel('Blog Titles')
    plt.ylabel('Number of Likes')

    plt.savefig('static/charts/blog_engagement.png')

    plt.clf()
    # clear figure syntax

    users = User.query.all()
    num = len(users)

    from datetime import datetime, timedelta

    now = datetime.utcnow()

    blogs = Blog.query.filter(Blog.timestamp >= now - timedelta(days=4)).all()

    # now -> 22 june 8 pm
    # now - timedelta(days=4) -> 18 june 8 pm 
    #  Blog.timestamp >= now - timedelta(days=4) will check if blog.timestamp after 18 june 8 pm 

    import random

    my_list = []

    for blog in blogs:
        age = (now - blog.timestamp).days
        value = 0
        limit = 5
        if age <= limit:
            print(blog.title)
            print(age)
            print(limit)
            value = ((age)/limit)*100
            print(value)
        

        # if age==0:
        #     value = '25%'
        # elif age==1:
        #     value = '50%'
        # elif age==2:
        #     value = '75%'
        # elif age==3:
        #     value = '100%'
        my_list.append((blog.title, value))    

    print(my_list)    

    return render_template('charts.html', num=num, my_list=my_list)

# from datetime import datetime, timedelta

# now = datetime.utcnow()

# blogs = Blog.query.filter(Blog.timestamp >= now - timedelta(days=4)).all()

# # now -> 22 june 8 pm
# # now - timedelta(days=4) -> 18 june 8 pm 
# #  Blog.timestamp >= now - timedelta(days=4) will check if blog.timestamp after 18 june 8 pm 

# for blog in blogs:
#     age = (now - blog.timestamp).days
#     print(blog.title)
#     if age==0:
#         print('25%')
#     elif age==1:
#         print('50%')
#     elif age==2:
#         print('75%')
#     elif age==3:
#         print('100%')
    