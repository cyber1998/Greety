# Ajax
from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from flask_session import Session
import datetime
import pymongo
import json
import uuid
from pymongo import MongoClient
import hashlib
from utility import User
from datetime import timedelta


app = Flask(__name__)
SESSION_TYPE = 'mongodb'
app.config.from_object(__name__)
Session(app)
 
# utility class instances declaration
user = User()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    try:
        if request.method == 'POST':
            email = request.json['username']
            password = request.json['password']
            client = MongoClient('localhost', 27017)
            db = client['greetydb']
            coll = db['users']
            result = coll.find({"email": email})
            if result != None:
                if user.get_hashed_password(email) == password:
                    session['username'] = email
                    return jsonify(message = "Logging you in ...")
                else:
                    return jsonify(message = "Invalid Credentials")
            else:
                return jsonify(message = "Login didn't work.")
    except:
        print("Login is not working")
        return render_template("login.html")

@app.route('/')
def index():
    if 'username' not in session:
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
            password = request.json['password']
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

@app.route('/manage/event/add', methods=['GET', 'POST'])
def manage_event():
# Manage the event
if request.method == 'POST':
        if 'username' in session:
            email = session['username']
        try:
            event_type = session['event']
            date = session['date']
            client = MongoClient('localhost', 27017)
            db = client['greetydb']
            coll = db['events']
            result = coll.update_one({"_id" : email}, { "$push" : {"events" : {"event_type" : event_type, "date": date}}}, upsert=True)
            print(result)
            return jsonify(message = "Event successfully added")
        except Exception as e:
            return jsonify(message = "Event not added. Please try again")
        else:
            return jsonify(message = "Please login to add events")
     
    
    
@app.route('/manage/event/', methods=['GET', 'POST'])
def add_details():

    if request.method == 'GET':
        session['date'] = request.json['date']
        session['event'] = request.json['event']
        return render_template('details.html')

    
      
    # if request.method == 'POST':
    #     if 'username' in session:
    #         email = session['username']
    #     else:
    #         return redirect('/')
    #     return jsonify(date = request.json['date'], event_type = request.json['event'])


@app.route('/logout')
def logout():
    if session:
        session.pop('username', None)
        return redirect("/")
    else:
        return render_template("application.html")


@app.before_request
def before_request():
    if 'username' in session:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes = 2)
        

if __name__ == '__main__':
    app.secret_key = uuid.uuid4
    app.run("localhost", 8000, debug=True)
