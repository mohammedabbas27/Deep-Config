import sys
from flask import Flask,request, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route('/data', methods=['POST'])
def data():
    name = request.form['Name']
    return name
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000,debug=True)