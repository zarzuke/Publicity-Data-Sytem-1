import sqlite3 
from flask import render_template, request,make_response,redirect,url_for,flash,session,g,jsonify
from library.DB import *
import subprocess

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
    return render_template("settings-record.html",user=g.user,filas=filas )

def try_record_file():
    filas = created_record()
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    
    for fila in filas:
        ws.append(fila)
    
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name='record.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

def try_delete(id):
    delete_projects(id)
    
def try_comments(user,worker,comments):
    update(user,worker,comments)
    return redirect(url_for("work",user=user))

def try_open(id, nombre):
    folder_path = f"trabajos\\{id}.{nombre}"
    try:
        os.startfile(folder_path)  # Para Windows
        return jsonify({"status": "success", "message": f"Opened folder: {folder_path}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    
def try_next(id,status):
    phase=check_phase(id)
    if status=="none":
        flash('Datos incorrectos seleccione estatus')
        return redirect(url_for('work', user=id))
    if phase[0][0]==4:
        save_record(id)
        delete_projects(id)
        flash('Trabajo Finalizado')
        return redirect(url_for("home"))
    elif phase[0][0]==1:
        if status=="approved":
            change_phase(id)
            flash('Fase Aprovada')
            return redirect(url_for('work', user=id))
    else:
        if status=="approved":
            change_phase(id)
            flash('Fase Aprovada')
            return redirect(url_for('work', user=id))
        elif status=="canceled":
            return_phase(id)
            flash('Fase Negada')
            return redirect(url_for('work', user=id))
