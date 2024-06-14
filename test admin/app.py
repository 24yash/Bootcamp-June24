# configs for the app
from flask import Flask
from application.database import db

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

    app.app_context().push()

    return app

app = create_all()

# other imports later on
from application.controllers import *
from application.models import *

if __name__ == "__main__":
    app.run()

# some comment