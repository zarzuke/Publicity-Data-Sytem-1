from flask import Flask,session,g
from library.URLs import *
from library.DB import delete_projects
app = Flask(__name__)

@app.route("/menu")
def index():
     return "interfaz principal"
@app.before_request
def before_request():
    if "username" in session:
        g.user = session["username"]
    else:
        g.user = None

@app.route("/registro",methods=["POST","GET"])
def signup():
    function = try_signup()
    return function

@app.route("/",methods=["POST","GET"])
def login():
    function = try_login()
    return function

@app.route("/home")
def home():
    function = try_home()
    return function

@app.route("/logout")
def logout():
    function = try_logout()
    return function

@app.route("/form", methods=["POST", "GET"])
def form():
    function = try_form()
    return function

@app.route("/Clients")
def clients():
    clients=try_clients()
    return  clients

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/settings/manager")
def settings_user():
    return render_template("settings-user.html")

@app.route("/work/<string:user>")
def work(user):
    id=try_work(user)
    return id

@app.route("/Clients/<string:client>")
def client(client):
    list=try_client(client)
    return list

@app.route("/design")
def design():
    return redirect(url_for("designer", designer=g.user[0]))

@app.route("/design/<string:designer>")
def designer(designer):
    function = try_design()
    return function

@app.route("/approval")
def approval():
    function = try_approval()
    return function

@app.route("/crafting")
def crafting():
    function = try_crafting()
    return function

@app.route("/ending")
def ending():
    function = try_ending()
    return function
    
@app.route("/delete/<string:id>")
def delete(id):
    delete_projects(id)
    return redirect(url_for("login"))

app.secret_key="12345"
if __name__== "__main__":
    app.run(debug=True,port=3000)