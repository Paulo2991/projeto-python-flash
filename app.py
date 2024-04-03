from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')

# Lista para armazenar os dados das pessoas cadastradas
pessoas = []

# Rota para exibir a página inicial com a lista de pessoas cadastradas e opções CRUD
@app.route('/')
def index():
    return render_template('index.html', pessoas=pessoas)

# Rota para cadastrar uma nova pessoa
@app.route('/cadastrar', methods=['POST'])
def cadastrar_pessoa():
    nome = request.form['nome']
    cpf = request.form['cpf']
    pessoas.append({'nome': nome, 'cpf': cpf})
    return redirect(url_for('index'))

# Rota para editar uma pessoa
@app.route('/editar/<cpf>', methods=['GET', 'POST'])
def editar_pessoa(cpf):
    for pessoa in pessoas:
        if pessoa['cpf'] == cpf:
            if request.method == 'POST':
                pessoa['nome'] = request.form['nome']
                pessoa['cpf'] = request.form['cpf']
                return redirect(url_for('index'))
            return render_template('editar.html', pessoa=pessoa)
    return "Pessoa não encontrada."

# Rota para excluir uma pessoa
@app.route('/excluir/<cpf>')
def excluir_pessoa(cpf):
    for pessoa in pessoas:
        if pessoa['cpf'] == cpf:
            pessoas.remove(pessoa)
            return redirect(url_for('index'))
    return "Pessoa não encontrada."

if __name__ == '__main__':
    app.run(debug=True)
