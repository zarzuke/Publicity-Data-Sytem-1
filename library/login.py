import sqlite3 
from flask import Flask, render_template, request,make_response,redirect,url_for,flash,session,g

def try_signup():
    bd = sqlite3.connect("library/database.db")
    cursor = bd.cursor()
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        cursor.execute("INSERT INTO users (userName,userPassword) VALUES (?, ?)", (username, password))
        bd.commit()
        flash("te has registrado de forma exitosa")
        bd.close()
        return redirect(url_for("login"))
    return render_template("signup.html")

def try_login():
    bd = sqlite3.connect("library/database.db")
    cursor = bd.cursor()
    if request.method=="POST":
        username=request.form["username"]
        password=(request.form["password"])
        cursor.execute("SELECT userPassword FROM users WHERE userName = ?" , (username,))
        pw=cursor.fetchone()
        if pw and pw[0]== password:
            session["username"]= username
            return redirect("/home")
        else:
                flash("credenciales invalidas verifique por favor")
    return render_template("index.html")

def try_home():
    if g.user:
        conn = sqlite3.connect('library/database.db')
        cursor = conn.cursor()
        print("Conexión exitosa a la base de datos")
        cursor.execute("""
                    SELECT projects.projectName, dateProject.projectDateStart, 
                    chargeProject.projectChargeTotalPayment,
                    clientProject.projectClientName, clientProject.projectClientNumber
                    FROM projects 
                    JOIN dateProject on projectDateId = projectDate
                    JOIN chargeProject on projectChargeId = projectCharge
                    JOIN clientProject on projectClientId = projectClient
                    """)
        filas = cursor.fetchall()
       
        return render_template("home.html",user=g.user,filas=filas)
    
    flash("Debes iniciar sesion Primero.")
    return render_template("index.html")

def try_logout():
    session.pop("username", None)
    flash("Cierre de Sesion")
    return redirect(url_for('login'))

def try_form():
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
