from flask import Flask, request, jsonify
from flask_cors import CORS

from app.functions import senha_criptografada, armazenar_senha, verificar_senha

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

    if not all([nome, email, telefone, senha]):
        return jsonify(erro="Todos os campos são obrigatórios."), 400

    try:
        armazenar_senha(nome, email, senha, telefone)
        return jsonify(msg="Usuário cadastrado com sucesso!"), 201
    except Exception as e:
        return jsonify(erro=str(e)), 500

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    print("Dados recebidos:", dados)  # Log dos dados recebidos

    nome = dados.get('nome')  
    senha = dados.get('senha')

    if not all([nome, senha]):
        return jsonify(erro="Nome ou senha incorretos"), 400

    resultado = verificar_senha(nome, senha)
    print("Resultado da verificação:", resultado)  # Log do resultado da verificação

    if resultado['sucesso'] == "True":
        return jsonify(msg=resultado['mensagem']), 200
    else:
        return jsonify(erro=resultado['mensagem']), 401

if __name__ == '__main__':
    app.run(debug=True)
