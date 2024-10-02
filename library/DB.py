import sqlite3 
from flask import Flask, render_template, request, make_response, redirect, url_for, flash, session, g, send_file  
import os
import openpyxl
import io

def project_inc():
    if request.method == "POST":
        title = request.form["title"]
        name = request.form["names"]
        lastname = request.form["surname"]
        phone = request.form["phone"]
        date = request.form["date"]
        job_type = request.form.getlist('job-type')
        total = int(request.form["total-cost"])
        mid = int(request.form["down-payment"])
        remaining = int(request.form["remaining"])
        total = request.form["total-cost"]
        mid = request.form["remaining"]
        remaining = request.form["down-payment"]
        details = request.form["description"]
        client_name=name+" "+lastname
        currency = request.form.get("currency")
        designer=request.form["designer"]
        crafter=request.form["crafter"]
        installer=request.form["installer"]

        conn = sqlite3.connect('library/database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO projects (projectName, projectDescript, projectPhase, projectDesigner, projectCrafter, projectInstaller) "
                    "VALUES (?,?,?,?,?,?)", (title, details,1,designer,crafter,installer,))

        id = cursor.lastrowid
        cursor.execute("UPDATE projects SET projectDate = ? WHERE projectId == ?",(id,id))
        cursor.execute("UPDATE projects SET projectCharge = ? WHERE projectId == ?",(id,id))
        
        cursor.execute("SELECT projectClientName FROM clientProject")
        clientes = cursor.fetchall()

        cursor.execute("SELECT COUNT(1) FROM clientProject WHERE projectClientName ==?",(client_name,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO clientProject (projectClientName, projectClientNumber) VALUES (?, ?)",
                    (client_name, phone))
        
        cursor.execute("""UPDATE projects SET projectClient = 
                       (SELECT projectClientId FROM clientProject WHERE projectClientName == ?) 
                       WHERE projectId == ?""",(client_name, id))

        cursor.execute("INSERT INTO chargeProject (projectChargeId, projectChargeCurrency, projectChargeInstallment, "
                   "projectChargeBalance, projectChargeTotalPayment) VALUES (?, ?, ?, ?, ?)",
                   (id, currency, remaining, mid, total))

        cursor.execute("INSERT INTO dateProject (projectDateId,projectDateStart) VALUES (?, ?)",
                   (id, date))
        
        for job in job_type:  
            cursor.execute("INSERT INTO ManyTypes (projectId,projectTypeId) VALUES (?, ?)", (id,job))

        conn.commit()
    
        direction = os.path.join(os.getcwd(), "trabajos", str(id)+"."+title)
        if not os.path.exists(direction):
            os.makedirs(direction)

    return redirect("/home")

def get_clients():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectClientName,ProjectClientNumber FROM clientProject")
    filas = cursor.fetchall()
    clientes= []
    for elemento in filas:
        if elemento not in clientes:
            clientes.append(elemento)
    return clientes

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
    details=filas[0][9].split('\n')
    info=list(filas[0])
    info[9]=details
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
    return info,tipos,id

def get_works_client(client):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("""
                SELECT p.projectName, dateProject.projectDateStart, 
                chargeProject.projectChargeTotalPayment,
                clientProject.projectClientName, clientProject.projectClientNumber,
                p.projectDescript, p.projectId, p.projectDesigner
                FROM projects p
                JOIN dateProject on projectDateId = projectDate
                JOIN chargeProject on projectChargeId = projectCharge
                JOIN clientProject on projectClientId = projectClient
                WHERE projectClientName == ?
                """,(client,))
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
            if f[7] == t[1]:
                lista.append(t[0])
        tipos.append(lista)

    conn.close()
    return filas,tipos

def change_phase(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectPhase FROM projects WHERE projectId == ?",(id,))
    phase = cursor.fetchall()
    print(phase)
    cursor.execute("""UPDATE projects SET projectPhase == ?+1 WHERE projectId == ?""",(phase[0][0],id))
    conn.commit()
    conn.close()
    
def check_phase(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectPhase FROM projects WHERE projectId == ?",(id,))
    phase = cursor.fetchall()
    return phase
    
def return_phase(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectPhase FROM projects WHERE projectId == ?",(id,))
    phase = cursor.fetchone()
    cursor.execute("""UPDATE projects SET projectPhase == ?-1 WHERE projectId == ?""",(phase[0][0],id))
    conn.commit()
    conn.close()

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
                """,(phase,))
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
    
def get_project_worker(worker):
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
                WHERE projectDesigner == ?
                """,(worker,))
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

def delete_projects(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectName FROM projects WHERE projectId == ?",(id,))
    title = cursor.fetchone()
    print(title)
    tables = [
    ("projects", "projectId"),
    ("chargeProject", "projectChargeId"),
    ("dateProject", "projectDateId"),
    ("ManyTypes", "projectId")
    ]

    for table, column in tables:
        cursor.execute(f"DELETE FROM {table} WHERE {column} == ?", (id,))

    conn.commit()
    conn.close()
    
    direction = os.path.join(os.getcwd(), "trabajos", str(id)+"."+title[0])
    if os.path.exists(direction):
        os.rename(direction,direction+"[Finished]")

def update(comments,user):
    if request.method == "POST":
        new_comments = request.form['comments']
        try:
            conn = sqlite3.connect('library/database.db')
            cursor = conn.cursor()
            if new_comments:
                cursor.execute("SELECT projectDescript, projectPhase FROM projects WHERE projectId = ?", (user,))
                result = cursor.fetchone()
                if result:
                    old_comments, phase = result
                    if old_comments:
                        all_comments = old_comments + f"\n" + new_comments
                        cursor.execute("UPDATE projects SET projectDescript = ? WHERE projectId = ?", (all_comments, user))
                    else:
                        cursor.execute("UPDATE projects SET projectDescript = ? WHERE projectId = ?", (new_comments, user))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            
def get_clients01():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectClientName FROM clientProject")
    names=cursor.fetchall()
    cursor.execute("SELECT projectClientNumber FROM clientProject")
    numbers=cursor.fetchall()
    conn.close()
    list=[]
    for i in names:
        new=i[0].split()
        list.append(new)
    return list,numbers

def save_record(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT projectClientName, projectChargeTotalPayment, projectDateStart
                    FROM projects
                    INNER JOIN clientProject ON projectClient = projectClientId
                    INNER JOIN chargeProject ON projectCharge = projectChargeId
                    INNER JOIN dateProject ON projectDate = projectDateId
                    WHERE projectId = ?""",(id,))
    record = cursor.fetchone()
    cursor.execute("""
                SELECT projectTypeName
                FROM ManyTypes m
                INNER JOIN typeProject t ON m.projectTypeId == t.projectTypeId
                WHERE projectId == ?
                """,(id,))
    types=cursor.fetchall()
    
    name,payment,date = record
    types_str = str()
    for t in types:
        types_str = types_str + "," + t[0]
    
    cursor.execute("INSERT INTO record (recordName,recordPayment,recordDate,recordTypeWork) VALUES (?,?,?,?)",(name,payment,date,types_str))
    conn.commit()
    conn.close()
    
def get_record():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM record")
    filas = cursor.fetchall()
    print(filas)
    conn.close()
    return filas

def get_workers():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT userName FROM users WHERE userRol= 'Designer'")
    design=cursor.fetchall()
    cursor.execute("SELECT userName FROM users WHERE userRol= 'Crafter'")
    craft=cursor.fetchall()
    cursor.execute("SELECT userName FROM users WHERE userRol= 'Installer'")
    install=cursor.fetchall()
    conn.close()
    return design,craft,install

import io
from openpyxl import Workbook

def created_record():
    # Conectar a la base de datos
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM record")
    filas = cursor.fetchall()
    conn.close()
    filas.insert(0,("id","Nombre","Pago","Fecha","TipoDeTrabajo"))
    print(filas)
    return filas

