from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
import os


# Configuración de la base de datos
dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/data.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search/",methods=["GET","POST"])
def search():
    nickname=request.args.get("nickname")
    user=Users.query.filter_by(username=nickname).first()

    if user:
        return user.username

    return "no existe"

@app.route("/registro/",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        hash = generate_password_hash(request.form["password"], method='pbkdf2:sha256')
        new_user=Users(username=request.form["username"],password=hash)
        db.session.add(new_user)
        db.session.commit()

        return "registro completo"

    return render_template("signup.html")

@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method==["POST"]:
            user = Users.query.filter_by(username=request.form["username"]).first()

            if user and check_password_hash(user.password,request.form["password"]):
                session["username"]=user.username
                return  "<h1>INICIO DE SESIÓN</h1>"
            return "credenciales invalidas"

    return render_template("login.html")

@app.route("/home")
def home():
    if "username" in session:
        return "You are %s" % escape(session["username"])

    return "You must log in first."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)