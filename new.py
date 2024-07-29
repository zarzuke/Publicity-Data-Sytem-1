from flask import Flask, render_template, request,make_response,redirect,url_for,flash,session,g
import sqlite3
from library.Test import *
from werkzeug.security import generate_password_hash, check_password_hash
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

app.secret_key="12345"
if __name__== "__main__":
    app.run(debug=True,port=3000)