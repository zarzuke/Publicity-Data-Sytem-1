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
                SELECT projectName, projectDateStart, 
                projectChargeTotalPayment,
                projectClientName, projectClientNumber,
                projectDescript,projectId
                FROM projects 
                JOIN dateProject on projectDateId = projectDate
                JOIN chargeProject on projectChargeId = projectCharge
                JOIN clientProject on projectClientId = projectClient
                """)
    filas = cursor.fetchall()
    cursor.execute("""
                SELECT projectTypeName, projectId
                FROM ManyTypes m
                INNER JOIN typeProject t ON m.projectTypeId == t.projectTypeId
                   """)
    types=cursor.fetchall()
    tipos=[]
    for f in filas:
        lista = [] 
        for t in types:
            if f[6] == t[1]:
                lista.append(t[0])
        tipos.append(lista)

    conn.close()
    return filas,tipos

def get_details(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("""
                SELECT projectName, 
                projectDateStart, projectDateFinished,
                projectChargeCurrency, projectChargeInstallment, projectChargeBalance, projectChargeTotalPayment,
                projectClientName, projectClientNumber,
                projectDescript
                FROM projects 
                JOIN dateProject on projectDateId = projectDate
                JOIN chargeProject on projectChargeId = projectCharge
                JOIN clientProject on projectClientId = projectClient
                WHERE projectId == ?
                """,(id,))
    filas = cursor.fetchall()
    cursor.execute("""
                SELECT projectTypeName
                FROM ManyTypes m
                INNER JOIN typeProject t ON m.projectTypeId == t.projectTypeId
                WHERE projectId == ?
                """,(id,))
    types = cursor.fetchall()
    tipos=[]
    for t in types:
        tipos.append(t[0])
    conn.close()
    return filas,tipos

def get_works_client(client):
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
                WHERE projectClientName == ?
                """,(client,))
    filas = cursor.fetchall()
    conn.close()
    return filas

def change_phase(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectPhase FROM projects WHERE projectId == ?",(id,))
    phase = cursor.fetchall()
    cursor.execute("""UPDATE projects SET projectPhase == ?+1 WHERE projectId == ?""",(phase[0],id))
    
def return_phase(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectPhase FROM projects WHERE projectId == ?",(id,))
    phase = cursor.fetchall()
    cursor.execute("""UPDATE projects SET projectPhase == ?-1 WHERE projectId == ?""",(phase[0],id))
    
def get_project_phase(phase):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("""
                SELECT projectName, projectDateStart, 
                projectChargeTotalPayment,
                projectClientName, projectClientNumber,
                projectDescript,projectId
                FROM projects 
                JOIN dateProject on projectDateId = projectDate
                JOIN chargeProject on projectChargeId = projectCharge
                JOIN clientProject on projectClientId = projectClient
                WHERE projectPhase == ?
                """(phase,))
    filas = cursor.fetchall()
    cursor.execute("""
                SELECT projectTypeName, projectId
                FROM ManyTypes m
                INNER JOIN typeProject t ON m.projectTypeId == t.projectTypeId
                   """)
    types=cursor.fetchall()
    tipos=[]
    for f in filas:
        lista = [] 
        for t in types:
            if f[6] == t[1]:
                lista.append(t[0])
        tipos.append(lista)

    conn.close()
    return filas,tipos


