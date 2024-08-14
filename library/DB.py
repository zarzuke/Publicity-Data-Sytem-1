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
        
        cursor.execute("SELECT projectId FROM projects ORDER BY projectId DESC LIMIT 1")
        id = cursor.fetchone()
        for job in job_type:  
            cursor.execute("INSERT INTO ManyTypes (projectId,projectTypeId) VALUES (?,?)", (id[0]+1,job))

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

def get_details(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("""
                SELECT projectName, 
                projectDateStart, projectDateFinished,
                projectChargeCurrency, projectChargeInstallment, projectChargeBalance, projectChargeTotalPayment,
                projectClientName, projectClientNumber,
                projectDescript,projectWorker
                FROM projects 
                JOIN dateProject on projectDateId = projectDate
                JOIN chargeProject on projectChargeId = projectCharge
                JOIN clientProject on projectClientId = projectClient
                WHERE projectId == ?
                """,(id,))
    filas = cursor.fetchall()
    conn.close()
    return filas

def get_types(type):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("""
                SELECT projectTypeName
                FROM ManyTypes m
                INNER JOIN typeProject t ON m.projectTypeId == t.projectTypeId
                WHERE projectId == ?
                """,(type,))
    filas = cursor.fetchall()
    conn.close()
    return filas

def get_works_client(client):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("""
                SELECT projectName, 
                projectDateStart, projectDateFinished,
                projectChargeCurrency, projectChargeInstallment, projectChargeBalance, projectChargeTotalPayment,
                projectClientName, projectClientNumber,
                projectDescript,projectWorker
                FROM projects 
                JOIN dateProject on projectDateId = projectDate
                JOIN chargeProject on projectChargeId = projectCharge
                JOIN clientProject on projectClientId = projectClient
                WHERE projectClientName == ?
                """,(client,))
    filas = cursor.fetchall()
    conn.close()
    return filas