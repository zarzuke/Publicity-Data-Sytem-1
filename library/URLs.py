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
        flash("Se ha registrado de forma exitosa")
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
                flash("Credenciales inválidas, intente de nuevo")
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
        cursor.execute("""
                    SELECT projects.projectId, typeProject.projectTypeName
                    FROM projects
                    INNER JOIN differentTypeProject on projects.projectId = differentTypeProject.keyProjectId 
                    INNER JOIN typeProject on differentTypeProject.keyProjectTypeId = typeProject.projectTypeId
                    """)
        folas = cursor.fetchall()
        
       
        return render_template("home.html",user=g.user,filas=filas)
    
    flash("Debe de iniciar sesión primero.")
    return render_template("index.html")

def try_logout():
    session.pop("username", None)
    flash("Sesión cerrada correctamente.")
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
        #cesar valnaskl
        client_name=name+" "+lastname

        conn = sqlite3.connect('library/database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO clientProject (projectClientName, projectClientNumber) VALUES (?, ?)",
                   (client_name, phone))
        
        cursor.execute("INSERT INTO chargeProject (projectChargeInstallment, "
                   "projectChargeBalance, projectChargeTotalPayment) VALUES (?, ?, ?)",
                   (remaining, mid, total))

        cursor.execute("INSERT INTO dateProject (projectDateStart) VALUES (?)",
                   (date,))
        cursor.execute("INSERT INTO typeProject (projectTypeName) VALUES (?)", (type,))

        cursor.execute("INSERT INTO projects (projectName) "
                    "VALUES (?)", (title,))
        conn.commit()

    return redirect("/home")


def try_clients():
    return render_template("clients.html")