from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_values = request.form.getlist('job-type')
        # Procesa los valores seleccionados (por ejemplo, imprímelos)
        return f"Valores seleccionados: {', '.join(selected_values)}"

    # Formulario HTML con los checkboxes
    return '''
        <form method="post">
            <label><input type="checkbox" name="job-type" value="Pendon"> Pendón</label>
            <label><input type="checkbox" name="job-type" value="Vinilo"> Vinilo</label>
            <!-- ...otros checkboxes... -->
            <input type="submit">
        </form>
    '''

app.run()