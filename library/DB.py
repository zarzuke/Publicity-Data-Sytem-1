import sqlite3 
from flask import Flask, render_template, request,make_response,redirect,url_for,flash,session,g

def project_inc():
    if request.method == "POST":
        title = request.form["title"]
        name = request.form["name"]
        lastname = request.form["surname"]
        phone = request.form["phone"]
        date = request.form["date"]
        job_type = request.form.getlist('job-type')  # Cambio de nombre aquí 
        total = request.form["total-cost"]
        mid = request.form["down-payment"]
        remaining = request.form["remaining"]
        details = request.form["description"]
        client_name=name+" "+lastname
        joblist=','.join(job_type)
        print(job_type)
        conn = sqlite3.connect('library/database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO clientProject (projectClientName, projectClientNumber) VALUES (?, ?)",
                   (client_name, phone))
        
        cursor.execute("INSERT INTO chargeProject (projectChargeInstallment, "
                   "projectChargeBalance, projectChargeTotalPayment) VALUES (?, ?, ?)",
                   (remaining, mid, total))

        cursor.execute("INSERT INTO dateProject (projectDateStart) VALUES (?)",
                   (date,))
        cursor.execute("INSERT INTO typeProject (projectTypeName) VALUES (?)", (joblist,))

        cursor.execute("INSERT INTO projects (projectName, projectDescript) "
                    "VALUES (?,?)", (title, details,))
        
        conn.commit()

    return redirect("/home")

def get_clients():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectClientName,ProjectClientNumber FROM clientProject")
    filas = cursor.fetchall()
    return filas

def get_project():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("""
                SELECT p.projectName, dateProject.projectDateStart, 
                chargeProject.projectChargeTotalPayment,
                clientProject.projectClientName, clientProject.projectClientNumber,
                p.projectDescript,p.projectWorker, p.projectId
                FROM projects p
                JOIN dateProject on projectDateId = projectDate
                JOIN chargeProject on projectChargeId = projectCharge
                JOIN clientProject on projectClientId = projectClient
                """)
    filas = cursor.fetchall()
    conn.close()
    return filas
