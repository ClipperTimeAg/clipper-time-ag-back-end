import bcrypt
import mysql.connector          

# Função para conexão com o Banco de Dados
def conectar_mysql():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="clipper_time_ag"
    )

# Função para criar um hash da senha
def senha_criptografada(senha):
    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hash_senha.decode('utf-8')  # armazenar como string

# Função para armazenar usuário e senha no banco
def armazenar_senha(name, email, senha, phone=""):
    conexao = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        hash_senha = senha_criptografada(senha)

        cursor.execute(
            "INSERT INTO usuarios (name, email, password_hash, phone) VALUES (%s, %s, %s, %s)",
            (name, email, hash_senha, phone)
        )
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
    except mysql.connector.Error as erro:
        print("Erro ao armazenar a senha:", erro)
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

# Função para verificar a senha do usuário
def verificar_senha(email, senha):
    conexao = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        cursor.execute("SELECT password_hash FROM usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()

        if not resultado:
            print("Usuário não encontrado.")
            return

        hash_senha = resultado[0]

        if bcrypt.checkpw(senha.encode('utf-8'), hash_senha.encode('utf-8')):
            print("Senha correta. Acesso permitido.")
        else:
            print("Senha incorreta. Acesso negado.")

    except mysql.connector.Error as erro:
        print("Erro ao verificar a senha:", erro)
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

# Exemplo de uso
nome = "Pedrp Toledo"
email = "pedro@gmail.com"
senha = "225896"
telefone = '(89) 91390-2590'

armazenar_senha(nome, email, senha,telefone)
verificar_senha(email, senha)
