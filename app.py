# configs for the app
from flask import Flask
from application.database import db

app = None

def create_all():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blogdata.sqlite3"
    db.init_app(app)

    app.app_context().push()

    return app

app = create_all()

# other imports later on
from application.controllers import *
from application.models import *

if __name__ == "__main__":
    app.run()

# some comment