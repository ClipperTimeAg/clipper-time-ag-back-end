from flask import Blueprint, request, jsonify
from flask import Flask
from app.functions import senha_criptografada
from app.functions import armazenar_senha

app = Flask(__name__)

@app.route('/rest/<texto>', methods=['GET'])
def hello(texto):
    return senha_criptografada(texto), 200

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.get_json()

    nome = dados.get('nome')
    email = dados.get('email')
    telefone = dados.get('telefone')
    senha = dados.get('senha')

    if not all([nome, email, telefone, senha]):
        return jsonify(erro="Todos os campos são obrigatórios."), 400

    resultado = armazenar_senha(nome, email, senha,telefone)
    return jsonify(resultado), 201

if __name__ == '__main__':
    app.run(debug=True)


