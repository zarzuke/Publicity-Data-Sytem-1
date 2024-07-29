import sqlite3 
from flask import Flask, render_template, request,make_response,redirect,url_for,flash,session,g

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

def get_clients():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectClientName,ProjectClientNumber FROM clientProject")
    filas = cursor.fetchall()
    return filas



