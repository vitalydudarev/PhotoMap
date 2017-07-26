from flask import Flask, render_template, request, send_file
from jinja2 import Template
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get_data")
def get_data():
    with open('data.txt', 'r') as outfile:
        j_data = outfile.read()
        return j_data

@app.route('/get_image/<id>')
def get_image(id):
    filename = os.path.join('/Users/vitaly/Downloads/thumbs', id)
    return send_file(filename, mimetype='image/gif')

if __name__ == "__main__":
     app.run(host='0.0.0.0')
    #app.run(debug=True)
