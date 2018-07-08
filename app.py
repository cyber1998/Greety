# Ajax
from flask import Flask, request, render_template, url_for, redirect, jsonify, session
from flask_session import Session
import datetime
import pymongo
import json
import uuid
from pymongo import MongoClient
import hashlib
from utility import User


# def __init__:
#     user = User()

user = User()


app = Flask(__name__)
SESSION_TYPE = 'mongodb'
app.config.from_object(__name__)
Session(app)
 

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    try:
        if request.method == 'POST':
            email = request.json['username']
            password = hashlib.sha256(request.json['password'].encode()).hexdigest()
            client = MongoClient('localhost', 27017)
            db = client['greetydb']
            coll = db['users']
            result = coll.find({"email": email})
            if result != None:
                session['username'] = email
                return jsonify(message = "Logging you in ...")
            else:
                return jsonify(message = "Login didn't work.")
    except:
        print("Login is not working")
        return render_template("login.html")

@app.route('/')
def index():
    if not session['username']:
        return render_template("application.html")
    else:
        firstname = user.get_first_name(session['username']) 
        return render_template("application.html", logged_user = firstname)

@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    try:
        if request.method == 'POST':
            email = request.json['email']
            password = hashlib.sha256(request.json['password'].encode()).hexdigest()
            firstname = request.json['firstname']
            lastname = request.json['lastname']
            client = MongoClient('localhost', 27017)
            db = client['greetydb']
            coll = db['users']
            if user.check_duplicate_user(email):
                return jsonify(response = "User already exists. Try logging in?")
            result = coll.insert_one({"email" : email,
                            "password" : password,
                            "firstname" : firstname,
                            "lastname":lastname})
            return jsonify(response = "You have successfully registered.")
    except Exception as e:
        print(e)
        return jsonify(response = "Error while connecting to the database")

@app.route('/manage/<event_type>')
def manage_event(event_type):
    # Manage the event
    pass

@app.route('/logout')
def logout():
    session.pop('username', None)

if __name__ == '__main__':
    app.secret_key = uuid.uuid4
    app.run("localhost", 8000, debug=True)

