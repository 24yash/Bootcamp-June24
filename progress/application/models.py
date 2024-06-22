# models for the app
from .database import db

from datetime import datetime


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id') ,primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id') ,primary_key=True)

class Like(db.Model):
    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id') ,primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id') ,primary_key=True) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True) # 20 here is the character limit on the username attribute
    password = db.Column(db.String(100), nullable=False)
    blogs = db.relationship('Blog', backref = 'author') # one to many
    # backref author creates a new attribute author on the Blog Model, which will allow us to access the User object associated with a blog
    # backref creates a pseudo column
    liked_blogs = db.relationship('Blog', backref='likers', secondary='likes') #many to many

    # we need some way for user to now like blogs, unlike blogs and to check if user has actually already liked a blog or not 
    def like(self, blog):
        # self is the user object who is currently logged in
        new_like = Like(user_id = self.id, blog_id = blog.id)
        db.session.add(new_like)
        db.session.commit()

    def unlike(self, blog):
        old_like = Like.query.filter_by(user_id = self.id, blog_id = blog.id).first()
        db.session.delete(old_like)
        db.session.commit()

# all() -> gets us all records in result
# count() -> gets us number of records in result
# first() -> gets us the first record from the result

    def has_liked(self, blog):
        return Like.query.filter_by(user_id = self.id, blog_id = blog.id).count() > 0
    

    # follow, unfollow, is_following
    # two more fn: followers (return list of followers) and following (return list of users the current user follow)

    def follow(self, other_user):
        # follower id is the current user who is following the other user that is the followed_id user 
        new_follow = Follow(follower_id = self.id, followed_id = other_user.id)
        db.session.add(new_follow)
        db.session.commit()

    def unfollow(self, other_user):
        old_follow = Follow.query.filter_by(follower_id=self.id, followed_id=other_user.id).first()
        db.session.delete(old_follow)
        db.session.commit()

    def is_following(self, other_user):
        check_follow = Follow.query.filter_by(follower_id=self.id, followed_id=other_user.id).first()
        return check_follow is not None
        # so if exists then True o/w False


# so two ways filter and filter_by. In filter_by params dont need Class name but filter params take Class name as well then the attribute. So filter takes logical operator and filter by takes assignment operator
    def following(self):
        return User.query.join(Follow, Follow.followed_id==User.id).filter(Follow.follower_id==self.id).all()
    # filter then join (TO BE TESTED)

    def followers(self):
        return User.query.join(Follow, Follow.follower_id==User.id).filter(Follow.followed_id==self.id).all()
    # filter then join (TO BE TESTED)

# nullable true means can be empty
#  nullable false means cannot be empty
# unique means each object must have different value for that particular attribute

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(150), nullable=True) # storing path for the image 
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    # default is a parameter accepted by Column that helps us provide an inital value to the attribute without having to specify it later on 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # tablename starts with small letter and foreign key acceptes the table.attribute as parameter

# like, follow and other things here 
# like is relationship from users to blogs
# follow is relationship from users to user 