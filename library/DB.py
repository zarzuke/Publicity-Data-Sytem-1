import sqlite3 
from flask import Flask, render_template, request, make_response, redirect, url_for, flash, session, g, send_file  
import os 

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
    
        direction = os.path.join(os.getcwd(), "trabajos", f"[{client_name}]-{title}")
        if not os.path.exists(direction):
            os.makedirs(direction)
    flash("Trabajo Creado Satisfactoriamente")
    return redirect("/home")

def get_clients():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectClientName,ProjectClientNumber,projectClientId FROM clientProject")
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
                projectDescript,projectId,projectPhase
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
                currencyTypeName, projectChargeInstallment, projectChargeBalance, projectChargeTotalPayment,
                projectClientName, projectClientNumber,
                projectDescript
                FROM projects 
                JOIN dateProject on projectDateId = projectDate
                JOIN chargeProject on projectChargeId = projectCharge
                JOIN clientProject on projectClientId = projectClient
				JOIN typeCurrency on currencyTypeId = projectChargeCurrency
                WHERE projectId == ?
                """,(id,))
    filas = cursor.fetchall()
    print(filas)
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
    print(phase)
    cursor.execute("""UPDATE projects SET projectPhase == ?-1 WHERE projectId == ?""",(phase[0],id,))
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

def update(user,worker,commments):
    print(user,worker,commments)
    new_comments = commments
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectDescript FROM projects WHERE projectId = ?", (user,))
    result = cursor.fetchall()
    old_comments= f"{result[0][0]}"
    all_comments = old_comments + f"\n" + worker+f": "+ new_comments
    cursor.execute("UPDATE projects SET projectDescript = ? WHERE projectId = ?", (all_comments, user))
    conn.commit()
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
    cursor.execute("""SELECT projectName ,projectClientName, projectChargeTotalPayment, projectChargeCurrency, projectDateStart
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
    
    name,client,payment,currency,date = record
    types_str = str()
    for t in types:
        types_str = types_str + "," + t[0]
    
    cursor.execute("INSERT INTO record (recordName,recordClient,recordPayment,recordCurrency,recordDate,recordTypeWork) VALUES (?,?,?,?,?,?)",(name,client,payment,currency,date,types_str))
    conn.commit()
    conn.close()
    
def get_record():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT recordName, recordClient, recordPayment, currencyTypeName, recordDate, recordTypeWork FROM record 
                INNER JOIN typeCurrency ON recordCurrency = currencyTypeId""")
    filas = cursor.fetchall()
    conn.close()
    
    cabecera = ['Nombre','Cliente','Precio','Divisa','Fecha','Tipo de Trabajo']
    filas.insert(0,cabecera)
    return filas

def record(client, date):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    filas = []  # Inicializar filas

    if client and date:
        date = date[6]+date[7]
        cursor.execute("""SELECT recordName, recordClient, recordPayment, currencyTypeName, recordDate, recordTypeWork 
                          FROM record 
                          INNER JOIN typeCurrency ON recordCurrency = currencyTypeId
                          WHERE recordClient = ? AND strftime('%W', recordDate) = ?""", (client, date))
    elif client:
        cursor.execute("""SELECT recordName, recordClient, recordPayment, currencyTypeName, recordDate, recordTypeWork 
                          FROM record 
                          INNER JOIN typeCurrency ON recordCurrency = currencyTypeId
                          WHERE recordClient = ?""", (client,))
    elif date:
        date = date[6]+date[7]
        cursor.execute("""SELECT recordName, recordClient, recordPayment, currencyTypeName, recordDate, recordTypeWork 
                          FROM record 
                          INNER JOIN typeCurrency ON recordCurrency = currencyTypeId
                          WHERE strftime('%W', recordDate) = ?""", (date,))
    else:
        cursor.execute("""SELECT recordName, recordClient, recordPayment, currencyTypeName, recordDate, recordTypeWork 
                          FROM record 
                          INNER JOIN typeCurrency ON recordCurrency = currencyTypeId""")
    
    filas = cursor.fetchall()
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

def create_client(client,number):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientProject (projectClientName,projectClientNumber) VALUES (?,?)",(client,number))
    conn.commit()
    conn.close()

def delete_client(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientProject WHERE projectClientId = ?",(id,))
    conn.commit()
    conn.close()
    
def update_currency(id,new):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectChargeInstallment FROM chargeProject WHERE projectChargeId = ?",(id,))
    balance=cursor.fetchone()
    intbas=int(balance[0])
    newbalance=int(new)-intbas
    cursor.execute("UPDATE chargeProject SET projectChargeTotalPayment = ?,projectChargeBalance = ?  WHERE projectChargeId=? ",(new,newbalance,id,))
    conn.commit()
    conn.close()
