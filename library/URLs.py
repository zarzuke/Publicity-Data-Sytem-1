import sqlite3 
from flask import render_template, request,make_response,redirect,url_for,flash,session,g,jsonify,send_file
from library.DB import *
import subprocess
import openpyxl
from openpyxl import load_workbook
import io

def try_signup():
    if request.method=="POST":
        bd = sqlite3.connect("library/database.db")
        cursor = bd.cursor()
        username=request.form["username"]
        password=request.form["password"]
        role=request.form["role"]
        cursor.execute("INSERT INTO users (userName,userPassword,userRol) VALUES (?, ?, ?)", (username, password, role,))
        bd.commit()
        bd.close()    
    return render_template("settings-user.html",user=g.user)

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
    match g.user[1]:
        case 'Administrator':
            filas,tipos=get_project()
            names,numbers=get_clients01()
            design,craft,install=get_workers()
            clients=zip(names,numbers)
            combine=zip(filas,tipos)
            return render_template("home.html",user=g.user,filas=combine,clients=clients,design=design,craft=craft,install=install)
        case 'Designer':
            return redirect(url_for("design", designer=g.user[1]))
        case 'Crafter':
            return redirect(url_for("crafting"))
        case 'Installer':
            return redirect(url_for("ending"))
        case _:
            flash("Debe de iniciar sesión primero.")
            return render_template("index.html")

def try_design():
    estado = 'Diseño'
    filas,tipos=get_project_phase(1)
    combine=zip(filas,tipos)
    return render_template("design.html",user=g.user,filas=combine,estado=estado)

    
def try_approval():
    estado = 'Aprobación'
    filas,tipos=get_project_phase(2)
    combine=zip(filas,tipos)
    return render_template("design.html",user=g.user,filas=combine,estado=estado)

def try_crafting():
    estado = 'Creación'
    filas,tipos=get_project_phase(3)
    combine=zip(filas,tipos)
    return render_template("design.html",user=g.user,filas=combine,estado=estado)

def try_ending():
    estado = 'Entrega'
    filas,tipos=get_project_phase(4)
    combine=zip(filas,tipos)
    return render_template("design.html",user=g.user,filas=combine,estado=estado)
    
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
    work,types,id=get_details(id)
    print(work,id)
    return render_template("work.html",user=g.user,details=work,types=types,nor=id)

def try_client(client):
    work,types=get_works_client(client)
    combine=zip(work,types)
    return render_template("design.html",user=g.user,filas=combine)

def try_settings():
    user = g.user
    print(user)
    return render_template("settings-user.html",user=g.user)

def try_record():
    filas = get_record()
    names,numbers=get_clients01()
    design,craft,install=get_workers()
    clients=zip(names,numbers)
    return render_template("settings-record.html",user=g.user,filas=filas,clients=clients)

def try_record_fildered(client,date):
    filas = record(client,date)
    
    cabecera = ['Nombre', 'Cliente', 'Precio', 'Divisa', 'Fecha', 'Tipo de Trabajo']
    filas.insert(0, cabecera)
    return filas

def try_record_file(client, date):
    filas = record(client, date)
    try:
        wb = load_workbook('Plantilla.xlsx')
        ws = wb.active
        
        start_row = 3
        for i, fila in enumerate(filas, start=start_row):
            for j, value in enumerate(fila, start=1):
                ws.cell(row=i, column=j, value=value)
        
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True, download_name='record.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        print(f"Error al procesar el archivo de Excel: {e}")
        return None

def try_delete(id):
    delete_projects(id)
    
def try_comments(user,worker):
    update(user,worker)
    return redirect(url_for("work",user=user))

def try_open(id, nombre):
    folder_path = f"trabajos\\{id}.{nombre}"
    try:
        os.startfile(folder_path)  # Para Windows
        return jsonify({"status": "success", "message": f"Opened folder: {folder_path}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    
def try_next(id):
    phase=check_phase(id)
    if phase[0][0]==4:
        save_record(id)
        delete_projects(id)
        return redirect(url_for("home"))
    else:
        change_phase(id)
        return redirect(url_for('work', user=id))
