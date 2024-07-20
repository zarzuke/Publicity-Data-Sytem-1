from flask import Flask, render_template, request,make_response,redirect,url_for,flash,session,g
import sqlite3 

def mi_decorador(func):
    def wrapper(*args, **kwargs):
        # Comportamiento adicional antes de ejecutar la función
        resultado = func(*args, **kwargs)
        # Comportamiento adicional después de ejecutar la función
        return resultado
    return wrapper


@mi_decorador
def formulario():
    bd=sqlite3.connect("database.db")
    cursor=bd.cursor()
    if request.method=="POST":
        title=request.form["title"]
        name=request.form["name"]
        lastname=request.form["surname"]
        phone=request.form["phone"]
        date=request.form["date"]
        type=request.form["job-type"]
        total=request.form["total-cost"]
        mid=request.form["down-payment"]
        remaining=request.form["remaining"]
        details=request.form["description"]
    
    return f"<p>{title} {name} {lastname} {phone} {date} {type} {total} {mid} {remaining} {details}</p>"
    
    """
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    bd.commit()
    flash("te has registrado de forma exitosa")
    bd.close()
    return redirect(url_for("login"))
    """