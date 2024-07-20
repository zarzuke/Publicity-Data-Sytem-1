from flask import Flask, render_template, request,make_response,redirect,url_for,flash,session,g
import sqlite3
from library.Test import *
from werkzeug.security import generate_password_hash, check_password_hash
import os
from markupsafe import escape

app= Flask(__name__)

bd=sqlite3.connect("DB.db")
cursor = bd.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
bd.commit()
bd.close()

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
    bd=sqlite3.connect("DB.db")
    cursor=bd.cursor()
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        bd.commit()
        flash("te has registrado de forma exitosa")
        bd.close()
        return redirect(url_for("login"))
        

    return render_template("signup.html")

@app.route("/",methods=["POST","GET"])
def login():
        if request.method=="POST":
            username=request.form["username"]
            password=(request.form["password"])
            bd=sqlite3.connect("DB.db")
            cursor=bd.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?" , (username,))
            pw=cursor.fetchone()
            if pw and pw[0]== password:
                session["username"]= username
                return redirect("/home")
            
            else:
                 flash("credenciales invalidas verifique por favor")

        
        return render_template("index.html")
@app.route("/home")
def home():
    if g.user:
        return render_template("home.html",user=g.user)
    
    flash("Debes iniciar sesion Primero.")
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Cierre de Sesion")
    return redirect(url_for('login'))

@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        title = request.form["title"]
        name = request.form["name"]
        lastname = request.form["surname"]
        phone = request.form["phone"]
        date = request.form["date"]
        job_type = request.form.get('value')  # Cambio de nombre aquí
        type = request.form.get('job-type')  # Cambio de nombre aquí
        total = request.form["total-cost"]
        mid = request.form["down-payment"]
        remaining = request.form["remaining"]
        details = request.form["description"]

    return f"<p>{title} {name} {lastname} {phone} {date} {job_type} {type} {total} {mid} {remaining} {details}</p>"

app.secret_key="12345"
if __name__== "__main__":
    app.run(debug=True,port=3000)