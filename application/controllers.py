#  routes will be present
from flask import Flask, render_template
# render template returning html files as response

from .models import *
#  to import everything we specify '*'

from flask import current_app as app
#  as is 'alias' 

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"