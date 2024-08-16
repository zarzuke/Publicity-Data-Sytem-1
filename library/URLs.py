import sqlite3 
from flask import Flask, render_template, request,make_response,redirect,url_for,flash,session,g
from library.DB import *

def try_signup():
    bd = sqlite3.connect("library/database.db")
    cursor = bd.cursor()
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        cursor.execute("INSERT INTO users (userName,userPassword) VALUES (?, ?)", (username, password))
        bd.commit()
        flash("Se ha registrado de forma exitosa")
        bd.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

def try_login():
    if g.user:
        home=try_home()
        return home

    bd = sqlite3.connect("library/database.db")
    cursor = bd.cursor()
    if request.method=="POST":
        username=request.form["username"]
        password=(request.form["password"])
        cursor.execute("SELECT userPassword FROM users WHERE userName = ?" , (username,))
        pw=cursor.fetchone()
        if pw and pw[0]== password:
            cursor.execute("SELECT userRol FROM users WHERE userName = ?" , (username,))
            rol=cursor.fetchone()
            session["username"]= [username,rol[0]]
            return redirect("/home")
        else:
                flash("Credenciales inválidas, intente de nuevo")
    return render_template("index.html")

def try_home():
    if g.user:
        filas,tipos=get_project()
        combine=zip(filas,tipos)
        return render_template("home.html",user=g.user,filas=combine)
    
    flash("Debe de iniciar sesión primero.")
    return render_template("index.html")

def try_logout():
    session.pop("username", None)
    flash("Sesión cerrada correctamente.")
    return redirect(url_for('login'))

def try_clients():
    if g.user:
        cliente=get_clients()
        return render_template("clients.html",user=g.user,cliente=cliente)
    
    flash("Debe de iniciar sesión primero.")
    return render_template("index.html")

def try_form():
    form=project_inc()
    return form

def try_work(id):
    work=get_details(id)
    return render_template("work.html",user=g.user,details=work)

def try_client(client):
    data=get_works_client(client)
    return render_template("Client.html",user=g.user,filas=data)