import sqlite3
from flask import Flask, request, g


DATABASE = 'pessoa.db'


app = Flask(__name__)
app.json.sort_keys = False


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    with app.app_context():
        sql_pragma_foreign_keys = "PRAGMA foreign_keys = ON;"
        get_db().cursor().execute(sql_pragma_foreign_keys)

        sql_create_departments_table = """
        CREATE TABLE IF NOT EXISTS pessoa (
            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL
        );
        """
        get_db().cursor().execute(sql_create_departments_table)


        get_db().commit()


@app.route("/pessoas", methods=["POST"])
def cadastrarPessoas():
    data = request.get_json()

    cursor = get_db().cursor()
    sqlInsertPessoas = "INSERT INTO pessoa (nome, cpf) VALUES (?, ?);"
    cursor.execute(sqlInsertPessoas, (data["nome"], data["cpf"]))
    get_db().commit()

    return {
        "id": cursor.lastrowid,
        "nome": data["nome"],
        "cpf": data["cpf"]    
        }


@app.route("/", methods=["GET"])
def listarPessoas():
    sqlSelectPessoas = "SELECT * FROM pessoa;"
    rows = get_db().cursor().execute(sqlSelectPessoas).fetchall()

    pessoas = []
    for row in rows:
        pessoa = {
            "id": row[0],
            "nome": row[1],
            "cpf": row[2]
        }
        pessoas.append(pessoa)

    return pessoas


@app.route("/pessoas/<int:id>", methods=["GET"])
def listarPessoasId(id):
    sqlSelectPessoasId = "SELECT * FROM pessoa WHERE id = ?;"
    row = get_db().cursor().execute(sqlSelectPessoasId, (id,)).fetchone()

    if not row:
        return {"message": "Department not found."}, 404

    pessoaListada = {
        "id": row[0],
        "nome": row[1],
        "cpf": row[2]    
    }

    return pessoaListada


@app.route("/pessoas/<int:id>", methods=["PUT"])
def editarPessoas(id):
    sqlSelectEditarPessoas = "SELECT * FROM pessoa WHERE id = ?;"
    row = get_db().cursor().execute(sqlSelectEditarPessoas, (id,)).fetchone()

    if not row:
        return {"message": "Department not found."}, 404

    data = request.get_json()

    if "nome" not in data or "cpf" not in data:
        return {"message": "Missing fields."}, 400

    sqlUpdatePessoas = "UPDATE pessoa SET nome = ?, cpf = ? WHERE id = ?;"
    get_db().cursor().execute(
        sqlUpdatePessoas,
        (data["nome"], data["cpf"], id)
    )
    get_db().commit()

    pessoa = {
        "id": id,
        "nome": data["nome"],
        "cpf": data["cpf"]
    }

    return pessoa


@app.route("/pessoas/<int:id>", methods=["DELETE"])
def deletarPessoas(id):
    sqlSelectDeletarPessoas = "SELECT * FROM pessoa WHERE id = ?;"
    row = get_db().cursor().execute(sqlSelectDeletarPessoas, (id,)).fetchone()

    if not row:
        return {"message": "Department not found."}, 404

    sqlDeletePessoas = "DELETE FROM pessoa WHERE id = ?;"
    get_db().cursor().execute(sqlDeletePessoas, (id,))
    get_db().commit()

    return "", 204

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)