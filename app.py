from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB = "contador.db"

# Inicializar base de datos si no existe
def init_db():
    if not os.path.exists(DB):
        with sqlite3.connect(DB) as conn:
            conn.execute("CREATE TABLE contador (id INTEGER PRIMARY KEY, valor INTEGER)")
            conn.execute("INSERT INTO contador (id, valor) VALUES (1, 0)")
            conn.commit()

def leer_contador():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT valor FROM contador WHERE id = 1")
        row = cur.fetchone()
        return row[0] if row else 0

def guardar_contador(valor):
    with sqlite3.connect(DB) as conn:
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
    port = int(os.environ.get("PORT", 8080))
app.run(host="0.0.0.0", port=port)


