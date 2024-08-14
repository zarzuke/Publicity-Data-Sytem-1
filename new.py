from flask import Flask,session,g
import sqlite3
from library.Test import *
import os
from markupsafe import escape
from library.URLs import *

app= Flask(__name__)

@app.route("/menu")
def index():
     return "interfaz principal"
@app.before_request
def before_request():
    if "username" in session:
        g.user = session["username"]
    else:
        g.user = None

@app.route("/registro",methods=["POST","GET"])
def signup():
    function = try_signup()
    return function

@app.route("/",methods=["POST","GET"])
def login():
    function = try_login()
    return function

@app.route("/home")
def home():
    function = try_home()
    return function

@app.route("/logout")
def logout():
    function = try_logout()
    return function

@app.route("/form", methods=["POST", "GET"])
def form():
    function = try_form()
    return function

@app.route("/Clients")
def clients():
    clients=try_clients()
    return  clients

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/work/<string:user>")
def work(user):
    id=try_work(user)
    return id

@app.route("/Clients/<string:client>")
def client(client):
    return client

app.secret_key="12345"
if __name__== "__main__":
    app.run(debug=True,port=3000)