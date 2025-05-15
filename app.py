from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Configuración para Railway
DB_PATH = os.path.join(os.getcwd(), "instance", "contador.db")  # Mejor ubicación
PORT = int(os.environ.get("PORT", 8080))  # Usa variable de entorno o 8080 por defecto

# Asegurar que existe el directorio instance
os.makedirs(os.path.join(os.getcwd(), "instance"), exist_ok=True)

def init_db():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("CREATE TABLE contador (id INTEGER PRIMARY KEY, valor INTEGER)")
            conn.execute("INSERT INTO contador (id, valor) VALUES (1, 0)")
            conn.commit()

def leer_contador():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT valor FROM contador WHERE id = 1")
        row = cur.fetchone()
        return row[0] if row else 0

def guardar_contador(valor):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE contador SET valor = ? WHERE id = 1", (valor,))
        conn.commit()

@app.route("/valor", methods=["GET"])
def obtener_valor():
    valor = leer_contador()
    return jsonify({"valor": valor})

@app.route("/incrementar", methods=["POST"])
def incrementar():
    valor = leer_contador() + 1
    guardar_contador(valor)
    return jsonify({"valor": valor})

if __name__ == "__main__":
    init_db()
    from waitress import serve
    serve(app, host="0.0.0.0", port=PORT)

