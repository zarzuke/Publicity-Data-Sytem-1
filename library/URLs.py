import sqlite3 
from flask import render_template, request,make_response,redirect,url_for,flash,session,g,jsonify,send_file
from library.DB import *
import subprocess
import openpyxl
from openpyxl import load_workbook
import io
import os

def try_signup():
    workers=get_users()
    if request.method=="POST":
        bd = sqlite3.connect("library/database.db")
        cursor = bd.cursor()
        username=request.form["username"]
        user_confirmation = user_exists(username)
        if user_confirmation:
            flash("El usuario ya está registrado en el sistema")
        else:
            password=request.form["password"]
            role=request.form["role"]
            cursor.execute("INSERT INTO users (userName,userPassword,userRol) VALUES (?, ?, ?)", (username, password, role,))
        bd.commit()
        bd.close()    
    return render_template("settings-user.html",user=g.user,workers=workers)

def try_login():
    if g.user==["vacio","vacio"]:
        render_template("index.html")
    else:
        home=try_home()
        return home
   
    if request.method=="POST":
        bd = sqlite3.connect("library/database.db")
        cursor = bd.cursor()
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
        case "vacio":
            flash("Debe de iniciar sesión primero.")
            return redirect(url_for('login'))

def try_design():
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    else:
        
        if g.user[1]=="Administrator":
            estado = 'Diseño'
            filas,tipos=get_project_phase(1)
            combine=zip(filas,tipos)
            return render_template("design.html",user=g.user,filas=combine,estado=estado)
        else:
            estado = 'Diseño'
            worker=g.user[0]
            filas,tipos=get_project_designer(worker)
            combine=zip(filas,tipos)
            return render_template("design.html",user=g.user,filas=combine,estado=estado)

    
def try_approval():
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    else:
        estado = 'Aprobación'
        filas,tipos=get_project_phase(2)
        combine=zip(filas,tipos)
        return render_template("design.html",user=g.user,filas=combine,estado=estado)

def try_crafting():
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    else:
        if g.user[1]=="Administrator":
            estado = 'Creacion'
            filas,tipos=get_project_phase(3)
            combine=zip(filas,tipos)
            return render_template("design.html",user=g.user,filas=combine,estado=estado)
        else:
            estado = 'Creación'
            worker=g.user[0]
            filas,tipos=get_project_crafter(worker)
            combine=zip(filas,tipos)
            return render_template("design.html",user=g.user,filas=combine,estado=estado)

def try_ending():
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    else:
        if g.user[1]=="Administrator":
            estado = 'Entrega'
            filas,tipos=get_project_phase(4)
            combine=zip(filas,tipos)
            return render_template("design.html",user=g.user,filas=combine,estado=estado)
        else:
            estado = 'Entrega'
            worker=g.user[0]
            filas,tipos=get_project_installer(worker)
            combine=zip(filas,tipos)
            return render_template("design.html",user=g.user,filas=combine,estado=estado)
    
def try_logout():
    session.pop("username", None)
    flash("Sesión cerrada correctamente.")
    return redirect(url_for('login'))

def try_clients():
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    else:
        cliente=get_clients()
        return render_template("clients.html",user=g.user,cliente=cliente)


def try_form():
    form=project_inc()
    return form

def try_work(id):
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    else:
        print(id)
        work,types,id=get_details(id)
        print(work,id)
        return render_template("work.html",user=g.user,details=work,types=types,nor=id)

def try_client(client):
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    
    elif g.user[1]!="Administrator":
        flash("No tienes Permisos para Acceder a este Modulo")
        return redirect("/home")
    
    else:
        work,types=get_works_client(client)
        combine=zip(work,types)
        return render_template("design.html",user=g.user,filas=combine)

def try_settings():
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    
    elif g.user[1]!="Administrator":
        flash("No tienes Permisos para Acceder a este Modulo")
        return redirect("/home")
    
    else:
        user = g.user
        print(user)
        return render_template("settings.html",user=g.user)

def try_record():
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    
    elif g.user[1]!="Administrator":
        flash("No tienes Permisos para Acceder a este Modulo")
        return redirect("/home")
    
    else:
        filas = get_record()
        names,numbers=get_clients01()
        design,craft,install=get_workers()
        clients=zip(names,numbers)
        return render_template("settings-record.html",user=g.user,filas=filas,clients=clients)

def try_record_fildered(client,date):
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    elif g.user[1]!="Administrator":
        flash("No tienes Permisos para Acceder a este Modulo")
        return redirect("/home")
    else:
        filas = record(client,date)
        cabecera = ['Nombre', 'Cliente', 'Precio', 'Divisa', 'Fecha', 'Tipo de Trabajo']
        filas.insert(0, cabecera)
        return filas

def try_record_file(client, date):
    filas = record(client, date)
    try:
        wb = load_workbook('library/Plantilla.xlsx')
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

def try_create_client(client_name):
    client_confirmation = client_exists(client_name)
    if client_confirmation:
        flash("El cliente ya está registrado en el sistema")
    else:
        country = request.form.get("country-code", "")
        phone = request.form.get("phone", "")
        if phone:
            number = f"{country} {phone}".strip()
            
        create_client(client_name,number)
        flash("Cliente Creado Satisfactoriamente")
    cliente=get_clients()
    return render_template("settings-client.html",user=g.user,cliente=cliente,os=os)
    
def try_edit_clients():
    if g.user==["vacio","vacio"]:
        flash("Debe de iniciar sesión primero.")
        return redirect(url_for('login'))
    else:
        cliente=get_clients()
        return render_template("settings-client.html",user=g.user,cliente=cliente,os=os)

def try_delete_client(id):
    delete_client(id)
    flash("Cliente Borrado Satisfactoriamente")
    cliente=get_clients()
    return render_template("settings-client.html",user=g.user,cliente=cliente,os=os)

def try_delete(id):
    delete_projects(id)
    flash("Trabajo Borrado Satisfactoriamente")
    return redirect("/home")
    
def try_comments(user,worker,comments):
    update(user,worker,comments)
    return redirect(url_for("work",user=user))

def try_open(id, title, client):
    folder_path = f"trabajos\\[{client}]-{title}"
    try:
        os.startfile(folder_path)  # Para Windows
        return f""
    except Exception as e:
        return f"Error en las Carpetas"
    
    
def try_next(id,status):
    phase=check_phase(id)
    if status=="none":
        flash('Datos incorrectos seleccione estatus')
        return redirect(url_for('work', user=id))
    
    if status=="canceled":
        if phase[0][0]==1:
            flash('Opcion incorrecta')
            if g.user[1]=="Administrator":
                return redirect(url_for('work', user=id))
            else:
                return redirect("/home")
        else:    
            return_phase(id)
            flash('Fase Negada')
            if g.user[1]=="Administrator":
                return redirect(url_for('work', user=id))
            else:
                return redirect("/home")
    
    if phase[0][0]==4:
        save_record(id)
        delete_projects(id)
        flash('Trabajo Finalizado')
        return redirect("/home")
    elif phase[0][0]==1:
        if status=="approved":
            change_phase(id)
            flash('Fase Aprobada')
            if g.user[1]=="Administrator":
                return redirect(url_for('work', user=id))
            else:
                return redirect("/home")
    else:
        if status=="approved":
            change_phase(id)
            flash('Fase Aprobada')
            if g.user[1]=="Administrator":
                return redirect(url_for('work', user=id))
            else:
                return redirect("/home")

def try_update_balance(id,charge,comments):
    update_currency(id,charge)
    text=f"Cambio de costo Total a {charge} por motivo de: {comments}"
    update(id,"Sistema",text)
    
def try_down_payment(id,down):
    update_down(id,down)
    down=float(down)
    text=f"El cliente hizo un abono de: {down}"
    update(id,"Sistema",text)
    
def try_edit_client(id):
    function = edit_client(id)
    return function

def try_edit_user():
    function = edit_client()
    return function

def try_delete_user(username):
    function = delete_user(username)
    return function