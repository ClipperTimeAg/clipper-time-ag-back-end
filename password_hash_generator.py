import smtplib
from email.mime.text import MIMEText
import bcrypt
import mysql.connector

# Configurações do e-mail
remetente = "an2767394@gmail.com"
senha_email = "zhaaaqxuwzwfbocr"                # sem espaços (Senha Gerada pelo google app)
destinatario = "anderson.ramos@procfit.com.br"  # Substitua por um e-mail real

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
        
        # Envio do e-mail após o cadastro
        enviar_email(email)

    except mysql.connector.Error as erro:
        print("Erro ao armazenar a senha:", erro)
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

# Função para enviar e-mail
def enviar_email(destinatario):
    assunto = "Confirme sua senha"
    corpo = "Olá,\n\nPor favor, confirme sua senha clicando no seguinte link: https://exemplo.com/confirmar"
    
    msg = MIMEText(corpo, "plain")
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remetente, senha_email)
            servidor.send_message(msg)
        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")

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
nome = "Otavio Brandão"
email = "Otario@gmail.com"
senha = "1234"
telefone = '(89) 91888-3000'

armazenar_senha(nome, email, senha, telefone)
verificar_senha(email, senha)
