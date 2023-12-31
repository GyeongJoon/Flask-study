from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome'

@app.route('/create/')
def create():
    return 'create'

@app.route('/read/<id>/')
def read(id):
    print(id)
    return 'Read '+id

app.run(debug=True)