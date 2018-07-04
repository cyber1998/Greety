# Ajax
from flask import Flask, request, render_template, url_for, redirect, jsonify
import datetime
import pymongo
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("application.html")

@app.route('/register')
def register():
    pass

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        return jsonify(username = username, password = password)

@app.route('/manage/<event_type>')
def manage_event(event_type):
    pass

@app.route('/logout')
def logout():
    session.pop('username', None)

app.run("localhost", 8000, debug=True)
