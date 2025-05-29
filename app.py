from flask import Flask, request, jsonify
from flask_cors import CORS

from app.functions import senha_criptografada, armazenar_senha

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

@app.route('/rest/<texto>', methods=['GET'])
def hello(texto):
    hash_texto = senha_criptografada(texto)
    return hash_texto, 200

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.get_json()

    nome = dados.get('nome')
    email = dados.get('email')
    telefone = dados.get('telefone')
    senha = dados.get('senha')

    # Validação simples
    if not all([nome, email, telefone, senha]):
        return jsonify(erro="Todos os campos são obrigatórios."), 400

    try:
        armazenar_senha(nome, email, senha, telefone)
        return jsonify(msg="Usuário cadastrado com sucesso!"), 201
    except Exception as e:
        return jsonify(erro=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
