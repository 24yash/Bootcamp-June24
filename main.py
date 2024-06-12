from flask import Flask, render_template

app = Flask(__name__)
# constructor provided by Flask to create a Flask web Application. 


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
# this ensures that app.run() is only called when the script is run directly. 