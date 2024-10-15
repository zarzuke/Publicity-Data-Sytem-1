import sqlite3 
from flask import Flask, render_template, request, make_response, redirect, url_for, flash, session, g, send_file  
import os 
import time

def project_inc():
    if request.method == "POST":
        title = request.form["title"]
        name = request.form["names"]
        lastname = request.form["surname"]
        country = request.form["country-code"]
        phone = request.form["phone"]
        date = request.form.get("date")
        job_type = request.form.getlist('job-type')
        total = float(request.form["total-cost"])
        mid = float(request.form["down-payment"])
        remaining = float(request.form["remaining"])
        total = request.form["total-cost"]
        mid = request.form["remaining"]
        remaining = request.form["down-payment"]
        details = request.form["description"]
        client_name=name+" "+lastname
        currency = request.form.get("currency")
        designer=request.form["designer"]
        crafter=request.form["crafter"]
        installer=request.form["installer"]
        fp=f"{country} {phone}"
        conn = sqlite3.connect('library/database.db')
        cursor = conn.cursor()
        if mid=="":
            mid=0
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
                    (client_name, fp))
        
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
    text=f"Nuevo Proyecto iniciado @{designer} esta a cargo del diseño"
    insertar_notificacion(text,g.user[0])
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
                projectDescript,projectPhase
                FROM projects 
                JOIN dateProject on projectDateId = projectDate
                JOIN chargeProject on projectChargeId = projectCharge
                JOIN clientProject on projectClientId = projectClient
				JOIN typeCurrency on currencyTypeId = projectChargeCurrency
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
                p.projectDescript, p.projectId, p.projectDesigner,projectPhase
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
                projectDescript,projectId,projectPhase
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
                projectDescript,projectId,projectPhase
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
    types_str = ','.join(t[0] for t in types)
    
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

def get_workers_id(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectDesigner,projectCrafter,projectInstaller FROM projects WHERE projectid=? ",(id,))
    design=cursor.fetchall()
    conn.close()
    return design

def get_users():
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT userName,userRol FROM users WHERE userRol != 'Administrator'")
    workers=cursor.fetchall()
    conn.close()
    return workers

def user_exists(username):
    conn = sqlite3.connect('library/database.db')  # Asegúrate de usar el path correcto a tu base de datos
    cursor = conn.cursor()
    cursor.execute("SELECT userId FROM users WHERE userName = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def client_exists(client_name):
    conn = sqlite3.connect('library/database.db')  # Asegúrate de usar el path correcto a tu base de datos
    cursor = conn.cursor()
    cursor.execute("SELECT projectClientId FROM clientProject WHERE projectClientName = ?", (client_name,))
    client = cursor.fetchone()
    conn.close()
    return client is not None
    
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
    intbas=float(balance[0])
    newbalance=float(new)-intbas
    cursor.execute("UPDATE chargeProject SET projectChargeTotalPayment = ?,projectChargeBalance = ?  WHERE projectChargeId=? ",(new,newbalance,id,))
    conn.commit()
    conn.close()

def get_project_designer(worker):
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
                WHERE projectDesigner == ? AND projectPhase == 1
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

def get_project_crafter(worker):
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
                WHERE projectCrafter == ? AND projectPhase == 3
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

def get_project_installer(worker):
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
                WHERE projectInstaller == ? AND projectPhase == 4
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

def update_down(id,down):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectChargeInstallment FROM chargeProject WHERE projectChargeId = ?",(id,))
    balance=cursor.fetchone()
    intbas=float(balance[0])
    newbalance=float(down)+intbas
    cursor.execute("SELECT projectChargeTotalPayment FROM chargeProject WHERE projectChargeId = ?",(id,))
    total=cursor.fetchone()
    ttotal=float(total[0])
    bl=ttotal-newbalance
    cursor.execute("UPDATE chargeProject SET projectChargeInstallment = ?,projectChargeBalance = ?  WHERE projectChargeId=? ",(newbalance,bl,id,))
    conn.commit()
    conn.close()
        
def edit_client(id):
    fp=str()
    name = request.form.get("names", "")
    lastname = request.form.get("surname", "")
    client_name = f"{name} {lastname}".strip()  # Asegúrate de que no quede espacio en blanco innecesario
    country = request.form.get("country-code", "")
    phone = request.form.get("phone", "")
    if phone:
        fp = f"{country} {phone}".strip()  # Asegúrate de que no quede espacio en blanco innecesario

    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    
    if client_name and not fp:  # Solo actualiza el nombre si no hay número
        cursor.execute("UPDATE clientProject SET projectClientName = ? WHERE projectClientId = ?",
                       (client_name, id))
    elif fp and not client_name:  # Solo actualiza el número si no hay nombre
        cursor.execute("UPDATE clientProject SET projectClientNumber = ? WHERE projectClientId = ?",
                       (fp, id))
    elif client_name and fp:  # Actualiza ambos si ambos están presentes
        cursor.execute("UPDATE clientProject SET projectClientName = ?, projectClientNumber = ? WHERE projectClientId = ?",
                       (client_name, fp, id))

    conn.commit()
    conn.close()
    return redirect(url_for('settings_client'))

def get_client_name(id):
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT projectClientName FROM clientProject WHERE projectClientId = ?",(id,))
    client_name = cursor.fetchone()
    conn.close()
    return client_name[0] if client_name else None

def edit_client():
    username = request.form.get("editUsername", "")
    new_username = request.form.get("new_username", "")
    role = request.form.get("editRole", "")
    password = request.form.get("password", "")
    conn = sqlite3.connect('library/database.db')
    cursor = conn.cursor()
    
    if new_username and not role and not password:  
        cursor.execute("UPDATE users SET userName = ? WHERE userName = ?",
                       (new_username, username))
    elif role and not username and not password:  
        cursor.execute("UPDATE users SET userRol = ? WHERE userName = ?",
                       (role, username))
    elif password and not username and not role:  
        cursor.execute("UPDATE users SET userPassword = ? WHERE userName = ?",
                       (password, username))
    elif new_username and role and password:  
        cursor.execute("UPDATE users SET userName = ?, userRol = ?, userPassword = ? WHERE userName = ?",
                       (new_username, role, password, username))

    conn.commit()
    conn.close()
    return redirect(url_for('settings_user'))

def delete_user(username):
    if username:
        conn = sqlite3.connect('library/database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE userName = ?",
                       (username,))
        conn.commit()
        conn.close()
        flash("Usuario Eliminado Correctamente")
        return redirect(url_for('settings_user'))
        
def get_titulo(id):
    connection = sqlite3.connect('library/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT projectName FROM projects WHERE projectId = ?",(id,))
    name=cursor.fetchone()[0]
    return name

def get_client_name(id):
    connection = sqlite3.connect('library/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT projectClientName FROM clientProject WHERE projectClientId = ?",(id,))
    name=cursor.fetchone()[0]
    return name

def insertar_notificacion(texto,user):
    date=time.localtime()
    dates=time.strftime("%d-%m-%Y %H:%S",date)
    connection = sqlite3.connect('library/database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO notifications (text,user,date) VALUES (?,?,?)', (texto,user,dates))
    connection.commit()
    connection.close()
    
def check_id(id):
    connection = sqlite3.connect('library/database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT projectID FROM projects")
    name=cursor.fetchall()
    for tupla in name:
        if int(id)==int(tupla[0]):
            return 1
    return 2
