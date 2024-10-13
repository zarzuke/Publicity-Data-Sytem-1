from flask import Flask,session,g,jsonify
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
        g.user = ["vacio","vacio"]

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
    function=try_settings()
    return function

@app.route("/settings/manager",methods=["POST","GET"])
def settings_user():
    function=try_signup()
    return function

@app.route("/settings/record",methods=['GET', 'POST'])
def settings_record():
    function = try_record()
    return function

@app.route('/update_grid', methods=['POST'])
def update_grid():
    client = request.form.get('client')
    date = request.form.get('date')
    print(date)
    filas = try_record_fildered(client,date)
    return jsonify(filas)

@app.route("/download", methods=["POST"])
def create_record():
    client = request.form.get('client')
    date = request.form.get('date')
    
    function = try_record_file(client, date)
    if function is None:
        return "Error processing the Excel file", 500
    return function

@app.route("/settings/client")
def settings_client():
    function = try_edit_clients()
    return function

@app.route('/work/<string:user>')
def work(user):
    session['user'] = user
    function = try_work(user)
    return function

@app.route('/work/balance')
def balance_update():
    id=request.args.get("id")
    charge=request.args.get("charge")
    reason=request.args.get("args")
    print(reason,id,charge)
    try_update_balance(id,charge,reason)
    return redirect(url_for('work', user=id))

@app.route('/work/down')
def down_update():
    id=request.args.get('id')
    down=request.args.get('down')
    try_down_payment(id,down)
    return redirect(url_for('work', user=id))
    
@app.route('/update')
def update():
    id=request.args.get("id")
    user=request.args.get("user")
    commets=request.args.get("comments")
    try_comments(id,user,commets)
    return redirect(url_for('work', user=id))

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
    #save_record(id)
    function=try_delete(id)
    return function

@app.route('/open/<string:id>/<string:nombre>/<string:cliente>')
def open_folder(id,nombre,cliente):
    try:
        return try_open(id, nombre, cliente)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/create-client',methods=["POST"])
def create_client():
    function=try_create_client()
    return function

@app.route('/delete-client/<string:id>')
def delete_client(id):
    function=try_delete_client(id)
    return function

@app.route('/next/<string:id>/<string:status>')
def next(id,status):
    function=try_next(id,status)
    return function
    


app.secret_key="12345"
if __name__== "__main__":
    app.run(debug=True,port=3000)