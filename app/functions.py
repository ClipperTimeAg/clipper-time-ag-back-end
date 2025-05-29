import smtplib
from email.mime.text import MIMEText
import bcrypt
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import logging
from typing import Optional, Dict

load_dotenv()  # lê o arquivo .env

remetente_email = os.getenv("REMETENTE_EMAIL")
remetente_nome = os.getenv("REMETENTE_NOME")
senha_email = os.getenv("SENHA_EMAIL")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def conectar_mysql():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="clipper_time_ag"
        )
        return conexao
    except Error as e:
        logging.error(f"Erro na conexão com MySQL: {e}")
        raise

def senha_criptografada(senha: str) -> str:
    """Gera hash bcrypt para a senha."""
    salt = bcrypt.gensalt()
    hash_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hash_senha.decode('utf-8')

def armazenar_senha(name: str, email: str, senha: str, phone: str = "") -> Dict[str, str]:
    """Armazena usuário e senha hash no banco e envia e-mail de confirmação."""
    conexao = None
    cursor = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT user_id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            raise ValueError("Email já cadastrado.")

        hash_senha = senha_criptografada(senha)

        cursor.execute(
            "INSERT INTO usuarios (name, email, password_hash, phone) VALUES (%s, %s, %s, %s)",
            (name, email, hash_senha, phone)
        )
        conexao.commit()
        logging.info(f"Usuário {email} cadastrado com sucesso.")

        enviar_email(email)

        return {"sucesso": "True", "mensagem": "Usuário cadastrado e e-mail enviado com sucesso."}

    except Error as e:
        logging.error(f"Erro ao armazenar a senha no banco: {e}")
        raise

    except Exception as e:
        logging.error(f"Erro: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def enviar_email(destinatario: str) -> None:
    """Envia email de confirmação para o destinatário."""
    assunto = "Cadastro realizado com sucesso"
    corpo = """Olá,

Seu cadastro foi realizado com sucesso em nossa plataforma.

Estamos felizes em tê-lo conosco! Caso tenha alguma dúvida ou precise de ajuda, não hesite em nos contatar.

Atenciosamente,
Equipe ClipperTime
"""

    msg = MIMEText(corpo, "plain")
    msg["Subject"] = assunto
    msg["From"] = f"{remetente_nome} <{remetente_email}>"
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remetente_email, senha_email)
            servidor.send_message(msg)
        logging.info("E-mail enviado com sucesso!")

    except smtplib.SMTPException as e:
        logging.error(f"Erro SMTP ao enviar o e-mail: {e}")
        raise

def verificar_senha(email: str, senha: str) -> bool:
    """Verifica se a senha informada corresponde ao hash armazenado."""
    conexao = None
    cursor = None
    try:
        conexao = conectar_mysql()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT password_hash FROM usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()

        if not resultado:
            logging.warning("Usuário não encontrado.")
            return False

        hash_senha = resultado[0]

        if bcrypt.checkpw(senha.encode('utf-8'), hash_senha.encode('utf-8')):
            logging.info("Senha correta. Acesso permitido.")
            return True
        else:
            logging.warning("Senha incorreta. Acesso negado.")
            return False

    except Error as e:
        logging.error(f"Erro ao verificar a senha: {e}")
        raise

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

