# HTTP REQUEST
# GET: Requests data from a specified resource.
# POST: Submits data to be processed to a specified resource.
# PUT: Updates a sepecified resource with provided data.
# DELETE: Deletes a sepecified resource.

# API: Application Programming Interface
# its a set of rules and protocols that allows different software apps to communicate with each other.

from flask_restful import Resource
from flask import request
from .models import *

# jsonify 

class HelloWorld(Resource):
    def get(self):
        return {'Hello': 'World!!'}

class BlogAPI(Resource):
    def get(self, id):
        # this is to send information about a specified blog 
        blog = Blog.query.filter_by(id = id).first()
        if blog is None:
            return {'error': 'Blog not found'}, 404
        
        return {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content
        }, 200
    
    def post(self):
        # this is to make a new blog in the app
        # mad course uses reqparse 
        args = request.get_json()
        new_blog = Blog(user_id=args['user_id'], title=args['title'], content=args['content'])
        db.session.add(new_blog)
        db.session.commit()
        return {
            'message': 'Blog is Created!',
            'blog_details': {
                'title': new_blog.title,
                'content': new_blog.content
            }
        }, 201
    
    def put(self, id):
        # this is to update an existing blog in the app
        # mad course uses reqparse 
        args = request.get_json()
        blog = Blog.query.filter_by(id=id).first()
        if blog is None:
            return {'error': 'Blog not found'}, 404
        
        blog.title = args['title']
        blog.content = args['content']
        db.session.commit()
        return {
            'message': 'Blog is Updated!',
            'blog_details': {
                'title': blog.title,
                'content': blog.content
            }
        }, 200
    
    def delete(self, id):
        blog = Blog.query.filter_by(id=id).first()
        if blog is None:
            return {'error': 'Blog not found'}, 404
        db.session.delete(blog)
        db.session.commit()
        return {'message':  'Blog Deleted!'}, 200
    
class BlogListAPI(Resource):
    def get(self):
        blogs = Blog.query.all()
        blogs_list = []
        for blog in blogs:
            blogs_list.append({
                'id': blog.id,
                'title': blog.title,
                'author': blog.author.username
            })
        return blogs_list, 200