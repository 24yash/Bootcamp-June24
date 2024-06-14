from flask import Flask, render_template, request

app = Flask(__name__)
# constructor provided by Flask to create a Flask web Application. 


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index", methods=['GET', 'POST'])
def index():
    some_var = "some data here"
    if request.method == 'POST':
        age = request.form['age']
        print(age)
        
    return render_template('index.html', some_var=some_var)

if __name__ == "__main__":
    app.run(debug=True)
# this ensures that app.run() is only called when the script is run directly. 