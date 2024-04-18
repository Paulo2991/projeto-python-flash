import sqlite3
from flask import Flask, request, g, jsonify,render_template,redirect, url_for


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


#   ROTA PARA CADASTRAR UMA NOVA PESSOA NA TABELA
@app.route("/pessoas", methods=["GET","POST"])
def cadastrarPessoas():
    if request.method == "POST":
        try:
            data = request.get_json()
            cursor = get_db().cursor()
            sqlInsertPessoas = "INSERT INTO pessoa (nome, cpf) VALUES (?, ?);"
            if "nome" not in data :
                return {"message": "nome é obrigatório."}, 400
            if "cpf" not in data :
                return {"message": "cpf é obrigatório."}, 400
            cursor.execute(sqlInsertPessoas, (data["nome"], data["cpf"]))
            get_db().commit()
            pessoas = []
            pessoa = {"id": cursor.lastrowid,"nome": data["nome"],"cpf": data["cpf"]}
            pessoas.append(pessoa)
            return redirect(url_for('listarPessoas'))
        except Exception as ex:
            return {"message": "erro interno do servidor."}, 500
    return render_template('cadastrar.html')

#   ROTA PARA LISTAR TODAD AS PESSOAS DA TABELA
@app.route("/", methods=["GET"])
def listarPessoas():
    try:
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
            # pessoasCadastradas = jsonify(pessoas)
        return render_template('index.html', pessoas=pessoas)
    except Exception as ex:
        return {"message": "erro interno do servidor."}, 500
    

#   ROTA PARA LISTAR PESSOA PELO ID
@app.route("/pessoas/<int:id>", methods=["GET"])
def listarPessoasId(id):
    try:    
        sqlSelectPessoasId = "SELECT * FROM pessoa WHERE id = ?;"
        row = get_db().cursor().execute(sqlSelectPessoasId, (id,)).fetchone()

        if not row:
            return {"message": "ID não existente."}, 404

        pessoaListada = {
            "id": row[0],
            "nome": row[1],
            "cpf": row[2]    
        }

        return jsonify(pessoaListada)
    except Exception as ex:
        return {"message": "erro interno do servidor."}, 500


#   ROTA PARA EDITAR UMA PESSOAS DA TABELA, SELECIONANDO PELO ID
#   METODO PUT, TODAS AS INFORMAÇÕES DA TABELA
@app.route("/editar/<int:id>", methods=["GET","POST","PUT"])
def editarPessoas(id):
   if request.method == "POST":
    try:
        sqlSelectEditarPessoas = "SELECT * FROM pessoa WHERE id = ?;"
        row = get_db().cursor().execute(sqlSelectEditarPessoas, (id,)).fetchone()

        if not row:
            return {"message": "ID não existente."}, 404

        data = request.get_json()

        if "nome" not in data :
            return {"message": "nome é obrigatório."}, 400
        if "cpf" not in data :
            return {"message": "cpf é obrigatório."}, 400

        sqlUpdatePessoas = "UPDATE pessoa SET nome = ?, cpf = ? WHERE id = ?;"
        get_db().cursor().execute(
            sqlUpdatePessoas,
            (data["nome"], data["cpf"], id)
        )
        get_db().commit()
        
        pessoas = []
        pessoa = {
            "id": id,
            "nome": data["nome"],
            "cpf": data["cpf"]
        }
        pessoas.append(pessoa)
        return redirect(url_for('index')) 
    except Exception as ex:
      return {"message": "erro interno do servidor."}, 500
    
    pessoas = []
    pessoa = {
      "id": id,
      "nome": data["nome"],
      "cpf": data["cpf"]
    }
   pessoas.append(pessoa)
   return render_template('editar.html', pessoa = pessoa) 

@app.route("/pessoas/<int:id>", methods=["DELETE"])
def deletarPessoas(id):
    try:
        sqlSelectDeletarPessoas = "SELECT * FROM pessoa WHERE id = ?;"
        row = get_db().cursor().execute(sqlSelectDeletarPessoas, (id,)).fetchone()

        if not row:
            return {"message":  "ID não existente."}, 404

        sqlDeletePessoas = "DELETE FROM pessoa WHERE id = ?;"
        get_db().cursor().execute(sqlDeletePessoas, (id,))
        get_db().commit()

        "", 204
    except Exception as ex:
        return {"message": "erro interno do servidor."}, 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
