from flask import Flask,session,g,jsonify,send_from_directory
from library.URLs import *
from library.DB import delete_projects
import os
from PIL import Image
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


UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def upload_file(name):
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        img = Image.open(file)
        new_filename = f"{name}.png"
        new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        img.save(new_filepath, 'PNG')
        return new_filename


def delete_image(name):
    if name:
        name = name+'.jpg'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    if os.path.exists(file_path):
        os.remove(file_path)

@app.route('/create-client',methods=["POST"])
def create_client():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    client_name = f"{firstname} {lastname}".strip()
    upload_file(client_name)
    
    function=try_create_client(client_name)
    return function

@app.route('/delete-client/<string:id>')
def delete_client(id):
    name = get_client_name(id)
    delete_image(name)
    function=try_delete_client(id)
    return function

@app.route('/next/<string:id>/<string:status>')
def next(id,status):
    function=try_next(id,status)
    return function

@app.route("/change-client/<string:id>", methods=["POST"])
def change_client(id):
    function = try_edit_client(id)
    return function

@app.route("/edit_user",methods=["POST"])
def edit_user():
    function= try_edit_user()
    return function

@app.route("/delete_user/<string:username>")
def delete_user(username):
    function= try_delete_user(username)
    return function

app.secret_key="12345"
if __name__== "__main__":
    app.run(debug=True,port=3000)