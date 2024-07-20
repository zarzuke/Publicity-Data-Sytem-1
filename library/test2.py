import sqlite3
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/muestras")
def conexion():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    print("Conexión exitosa a la base de datos")
    cursor.execute("""
                    SELECT projects.projectName, dateProject.projectDateStart, 
                    chargeProject.projectChargeTotalPayment,
                    clientProject.projectClientName, clientProject.projectClientNumber
                    FROM projects 
                    JOIN dateProject on projectDateId = projectDate
                    JOIN chargeProject on projectChargeId = projectCharge
                    JOIN clientProject on projectClientId = projectClient
                    """)
    filas = cursor.fetchall()
    print(filas)
    cursor.execute("""
                    SELECT projects.projectId, typeProject.projectTypeName
                    FROM projects
                    INNER JOIN differentTypeProject on projects.projectId = differentTypeProject.keyProjectId 
                    INNER JOIN typeProject on differentTypeProject.keyProjectTypeId = typeProject.projectTypeId
                    """)
    folas = cursor.fetchall()
    print(folas)

    return f"<h1>{filas}</h1><h1> {folas}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
