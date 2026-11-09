import os
import time

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


def init_db():
    for _ in range(10):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS notas ("
                "id SERIAL PRIMARY KEY, "
                "texto TEXT NOT NULL, "
                "creada TIMESTAMP DEFAULT NOW())"
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except psycopg2.OperationalError:
            time.sleep(2)
    raise RuntimeError("No se pudo conectar a la base de datos")


@app.route("/")
def inicio():
    return jsonify({"mensaje": "API de notas funcionando"})


@app.route("/notas", methods=["POST"])
def crear_nota():
    texto = request.get_json().get("texto", "")
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO notas (texto) VALUES (%s) RETURNING id", (texto,))
    nota_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": nota_id, "texto": texto}), 201


@app.route("/notas", methods=["GET"])
def listar_notas():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, texto, creada FROM notas ORDER BY id")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(
        [{"id": f[0], "texto": f[1], "creada": f[2].isoformat()} for f in filas]
    )


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)