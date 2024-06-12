# models for the app
from .database import db

from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True) # 20 here is the character limit on the username attribute
    password = db.Column(db.String(100), nullable=False)

# nullable true means can be empty
#  nullable false means cannot be empty
# unique means each object must have different value for that particular attribute

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_1 = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(150), nullable=True) # storing path for the image 
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    # default is a parameter accepted by Column that helps us provide an inital value to the attribute without having to specify it later on 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # tablename starts with small letter and foreign key acceptes the table.attribute as parameter

# like, follow and other things here 