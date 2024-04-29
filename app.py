import sqlite3
from flask import Flask, request,render_template,redirect, url_for,flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'
dbName = 'cadastro.db'

def criarTabela():
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pessoa (
            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL
        );''')
    conn.commit()
    conn.close()



#   ROTA PARA CADASTRAR UMA NOVA PESSOA NA TABELA
@app.route("/cadastrar", methods=["GET","POST"])
def cadastrarPessoas():
    if request.method == "POST":
     conn = sqlite3.connect(dbName)
     c = conn.cursor()
     c.execute("INSERT INTO pessoa (nome, cpf) VALUES (?, ?)", (request.form['nome'], request.form['cpf']))
     conn.commit()
     conn.close()
     flash('Cadastro realizado com sucesso!', 'success')
     return redirect(url_for('index'))
    return render_template('cadastrar.html')

#   ROTA PARA LISTAR TODAD AS PESSOAS DA TABELA
@app.route("/")
def index():
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute("SELECT * FROM pessoa")
    pessoas = c.fetchall()
    conn.close()
    return render_template('index.html', pessoas=pessoas)

#   ROTA PARA LISTAR PESSOA PELO ID



#   ROTA PARA EDITAR UMA PESSOAS DA TABELA, SELECIONANDO PELO ID
#   METODO PUT, TODAS AS INFORMAÇÕES DA TABELA
@app.route("/editar/<int:id>", methods=["GET","POST"])
def editarPessoas(id):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    if request.method == 'POST':        
        c.execute("UPDATE pessoa SET nome=?, cpf=? WHERE id=?", (request.form['nome'], request.form['cpf'], id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM pessoa WHERE id=?", (id,))
        pessoa = c.fetchone()
        conn.close()
        flash('Editado realizado com sucesso!', 'success')
        return render_template('editar.html', pessoa=pessoa)

@app.route("/pessoas/<int:id>")
def deletarPessoas(id):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute("DELETE FROM pessoa WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Registro excluido com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    criarTabela()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)