# configs for the app
from flask import Flask
from application.database import db

from flask_restful import Api
from application.resources import *

app = None

def create_all():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blogdata.sqlite3"
    db.init_app(app)

    # secret key = 2
    # data = 3

    # encrypt = 2*3 = 6
    # decrypt = 6/2 = 3

    app.secret_key = 'anythingCanbePuthere'
    # it is used to encrypt the session data before it's stored. 

    app.config['UPLOAD_FOLDER'] = 'static/images'

    app.app_context().push()

    api = Api(app)
    api.add_resource(HelloWorld, '/api/helloworld')

    api.add_resource(BlogAPI, '/api/blog/<int:id>', '/api/blog')

    api.add_resource(BlogListAPI, '/api/blogs')

    # api object method call here 

    return app

app = create_all()

# other imports later on
from application.controllers import *
from application.models import *

if __name__ == "__main__":
    app.run()

# some comment