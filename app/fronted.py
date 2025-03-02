from flask import Flask, render_template, request, jsonify
import requests

# Inicializar Flask
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return render_template('index.html')  # Renderizamos el archivo HTML

@flask_app.route('/send_teorema', methods=['POST'])
def send_teorema():
    teorema = request.form['teorema']
    if teorema:
        # Enviar el teorema a la API FastAPI
        response = requests.post('http://localhost/add_theorem', json={"teorema": teorema})
        if response.status_code == 200:
            return jsonify({"response": response.json()})
        else:
            return jsonify({"error": "Hubo un problema con la API de FastAPI."})
    return jsonify({"error": "No se ingresó ningún teorema."})

# Correr la app Flask
if __name__ == "__main__":
    flask_app.run(debug=True, port=5000)