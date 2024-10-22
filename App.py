from flask import Flask, session, g, jsonify, request, redirect, url_for, send_from_directory, render_template,current_app
from flask_socketio import SocketIO, emit
from library.URLs import *
import os
from PIL import Image


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
socketio = SocketIO(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Variable global para almacenar el usuario actual
current_user = None

def check_db_for_updates():
    global current_user
    last_update = None
    while True:
        connection = sqlite3.connect('library/database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT MAX(id) FROM notifications')
        latest_update = cursor.fetchone()[0]
        if last_update is None:
            last_update = latest_update
        if latest_update != last_update:
            last_update = latest_update
            cursor.execute('SELECT text FROM notifications WHERE id = ?', (latest_update,))
            texto = cursor.fetchone()[0]
            cursor.close()
            # Emitir notificación si el usuario actual es administrador
            if current_user and current_user[1] == "Administrator":
                socketio.emit('notification', {'message': texto})
        
        time.sleep(1)

@app.before_request
def before_request():
    global current_user
    if "username" in session:
        g.user = session["username"]
        current_user = session["username"]
    else:
        g.user = ["vacio", "vacio"]
        current_user = g.user

@app.route("/", methods=["POST", "GET"])
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
    clients = try_clients()
    return clients

@app.route("/settings")
def settings():
    function = try_settings()
    return function

@app.route("/settings/manager", methods=["POST", "GET"])
def settings_user():
    function = try_signup()
    return function

@app.route("/settings/record", methods=['GET', 'POST'])
def settings_record():
    function = try_record()
    return function

@app.route('/update_grid', methods=['POST'])
def update_grid():
    client = request.form.get('client')
    date = request.form.get('date')
    filas = try_record_fildered(client, date)
    return jsonify(filas)

@app.route("/download", methods=["POST"])
def create_record():
    client = request.form.get('client')
    date = request.form.get('date')
    file_format = request.form.get('format')
    function = try_record_file(client, date,file_format)
    if function is None:
        return "Error processing the file", 500
    else:
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
    id = request.args.get("id")
    charge = request.args.get("charge")
    reason = request.args.get("args")
    try_update_balance(id, charge, reason)
    return redirect(url_for('work', user=id))

@app.route('/work/down')
def down_update():
    id = request.args.get('id')
    down = request.args.get('down')
    try_down_payment(id, down)
    return redirect(url_for('work', user=id))

@app.route('/update')
def update():
    id = request.args.get("id")
    user = request.args.get("user")
    comments = request.args.get("comments")
    try_comments(id, user, comments)
    return redirect(url_for('work', user=id))

@app.route("/Clients/<string:client>")
def client(client):
    list = try_client(client)
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
    function = try_delete(id)
    return function

@app.route('/open/<string:id>/<string:nombre>/<string:cliente>')
def open_folder(id, nombre, cliente):
    try:
        return try_open(id, nombre, cliente)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

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
        name = name + '.png'
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    if os.path.exists(file_path):
        os.remove(file_path)

@app.route('/create-client', methods=["POST"])
def create_client():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    client_name = f"{firstname} {lastname}".strip()
    upload_file(client_name)
    function = try_create_client(client_name)
    return function

@app.route('/delete-client/<string:id>')
def delete_client(id):
    name = get_client_name(id)
    delete_image(name)
    function = try_delete_client(id)
    return function

@app.route('/next/<string:id>/<string:status>')
def next(id, status):
    cdr=request.args.get('cdr')
    function = try_next(id, status,cdr)
    return function

@app.route("/change-client/<string:id>", methods=["POST"])
def change_client(id):
    name = request.form.get("names", "")
    lastname = request.form.get("surname", "")
    client_name = f"{name} {lastname}".strip()
    file = request.files.get('photo')
    oldname = get_client_name(id)
    if not file or file.filename == '':
        if client_name == "":
            return redirect(request.url)
        else:
            actual = os.path.join(app.config['UPLOAD_FOLDER'], f"{oldname}.png")
            nuevo_nombre = os.path.join(app.config['UPLOAD_FOLDER'], f"{client_name}.png")
            os.rename(actual, nuevo_nombre)

    if file:
        if client_name == "":
            client_name = oldname
        img = Image.open(file)
        new_filename = f"{client_name}.png"
        new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        img.save(new_filepath, 'PNG')
                
    function = try_edit_client(id)
    return function

@app.route("/edit_user", methods=["POST"])
def edit_user():
    function = try_edit_user()
    return function

@app.route("/delete_user/<string:username>")
def delete_user(username):
    function = try_delete_user(username)
    return function

# Ruta para recibir notificaciones
@app.route('/send_notification', methods=['POST'])
def send_notification():
    message = request.form.get('message')
    if message:
        socketio.emit('notification', {'message': message})
    return f"Exito"

# Ruta para mostrar notificaciones
@app.route('/display_notifications')
def display_notifications():
    return render_template('display_notifications.html')

@socketio.on('connect')
def handle_connect():
    pass

@app.route('/notifications')
def notifications():
    function = try_show_notifications()
    return function

@app.route('/show-notifications')
def show_notifications():
    rows = get_notifications()
    # Formateamos la respuesta para que sea compatible con DataTables
    return jsonify({"data": rows})

if __name__ == "__main__":
    socketio.start_background_task(check_db_for_updates)
    socketio.run(app, host='0.0.0.0',debug=True, port=3000)
