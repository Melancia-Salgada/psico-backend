from http.client import HTTPException
from typing import List
from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from Controllers.Controller_user import User
from Controllers.controller_planoDeAcao import ControllerPlanoDeAcao
from models.userModel import Psicologo
from models.planoDeAcaoModel import PlanoDeAcao
import random
import string
 
 
# modelo de email a ser enviado
class EmailSchema(BaseModel):
    email: List[EmailStr]
 
# configurações de conexão com o email, está com bug na senha, que deve ser gerada pelo gmail
conf = ConnectionConfig(
    MAIL_USERNAME ="dsm.devspsi@gmail.com",
    MAIL_PASSWORD = "geqe cqdo nxnn azsi",
    MAIL_FROM = "dsm.devspsi@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False
)
 
 
fm = FastMail(conf)
 
html= ""

class ControllerEmail:
    def __init__(self) -> None:
      pass

    @staticmethod
    def gerar_string_aleatoria(digitos: int = 6) -> str:
        return ''.join(random.choices(string.digits, k=digitos))
       
    @staticmethod
    async def enviarEmailConfirmacao(user: dict): 
        try:
            emailusuario = user["email"]
            username = user["username"]
            codigo = ControllerEmail.gerar_string_aleatoria()
           
       
            html = f"""
                <h1>Olá, {username}</h1>
                <p>Recebemos a sua solicitação de cadastro na EasyPsi</p>
                <br>
                <p>Segue o código abaixo abaixo para primeiro login na plataforma:</p>
                <p><strong>{codigo}</strong></p>
                <br>
                <p>Se você não solicitou esse e-mail de código de login, não precisa se preocupar</p>
                <p>Basta ignorar esse e-mail</p>
                <br>
                
                <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
                <p>Atenciosamente,</p>
                <p>Equipe da EazyPsi</p>
            """.format(username=username)
    
            message = MessageSchema(
                subject="Código de login - EazyPsi",
                recipients=[emailusuario],
                body=html,
                subtype=MessageType.html
            )
 
            # Envio do e-mail
            await fm.send_message(message)

            return codigo
        except Exception as e:
            # Tratamento de exceções
            print("Erro ao enviar e-mail:", e)


    async def emailLembreteConsulta(self,email: str, link_meet:str):
        try:
            emailusuario = email
            
        
            
            html = f"""
                <h1>Olá,</h1>
                <p>Este é um lembrete da sua sessão de terapia.</p>
                <br>
                <br>
                <p>Segue abaixo o link da consulta:</p>
                <br>
                <p>{link_meet}</p>
                <br>
                <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
                <p>Atenciosamente,</p>
                <p>EasyPsi</p>
            """
            
            message = MessageSchema(
                subject="Lembrete de sessão de terapia",
                recipients=[emailusuario],
                body=html,
                subtype=MessageType.html
            )
            
            # Envio do e-mail
            await fm.send_message(message)
        except Exception as e:
            # Tratamento de exceções
            print("Erro ao enviar e-mail:", e)
    
@staticmethod        
async def emailPlanoDeAcao(planoDeAcao : PlanoDeAcao):
    try:
        email = planoDeAcao.email
        plano = planoDeAcao.texto
        
        html = f"""
            <h1>Olá,</h1>
            <p>Um novo plano de ação foi criado por seu/sua psicólogo/a:</p>
            <br>
            <br>
            <p>{plano}</p>
            <br>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>EasyPsi</p>
        """
        
        message = MessageSchema(
            subject = "Novo plano de ação",
            recipients = [email],
            body = html,
            subtype= MessageType.html
        )
        
        ControllerPlanoDeAcao.insertPlanoDeAcao(planoDeAcao)
        await fm.send_message(message)
    except Exception as e:
        print("Erro ao enviar o email", e)
        
@staticmethod
async def emailEsqueceuSenha(user: User,token:str): #, token: str
    try:
        emailusuario = user["email"]
        username = user["name"]
        redefinirURL = f"http://127.0.0.1:3000/redefinir-senha?token={token}"
 
        html = """
            <h1>Olá, {username}</h1>
            <p>Recebemos recentemente um pedido de recuperação de senha da sua conta cadastrada na InkDash</p>
            <br>
            <p>Se você não solicitou esse e-mail de redefinição de senha, não precisa se preocupar</p>
            <p>Basta ignorar esse e-mail</p>
            <br>
            <p>Clique no link abaixo para redefinir sua senha:</p>
            <p><a href="{redefinirURL}">Link para redefinição de senha</a></p>
            <br>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>Equipe da InkDash</p>
        """.format(username=username, redefinirURL= redefinirURL)
 
        message = MessageSchema(
            subject="Recuperação de Senha - InkDash",
            recipients=[emailusuario],
            body=html,
            subtype=MessageType.html
        )
 
        # Envio do e-mail
        await fm.send_message(message)
    except Exception as e:
        # Tratamento de exceções
        print("Erro ao enviar e-mail:", e)

async def senhaRedefinida(user: User):
    try:
        emailusuario = user["email"]
        html = """
            <h1>Olá, {username}</h1>
            <p>Sua senha foi redefinida com sucesso</p>
            <p>Basta utilizar a nova senha cadastrada no link que te enviamos anteriormente</p>
            <br>
            <p>Ps: Não esqueça de nunca compartilhar as suas senhas com ninguém.</p>
            <br>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>Equipe da InkDash</p>
        """.format(username=user["name"])
 
        message = MessageSchema(
            subject="A redefinição de senha foi um sucesso! - InkDash",
            recipients=[emailusuario],
            body=html,
            subtype=MessageType.html
        )
 
        # Envio do e-mail
        await fm.send_message(message)
    except Exception as e:
        # Tratamento de exceções
        print("Erro ao enviar e-mail:", e)


#Emails procedimentos

async def email24Antes(email: str):
    try:
        emailusuario = email
       
        
        html = """
            <h1>Olá,</h1>
            <p>Este é um lembrete do seu agendamento de tatuagem na InkDash amanhã.</p>
            <br>
            <br>
            <p>Estamos ansiosos para vê-lo!</p>
            <p>Se você tiver alguma dúvida ou precisar reagendar, por favor entre em contato conosco.</p>
            <br>
            <p>Este é um e-mail automático, não é preciso responder &#128521;</p>
            <p>Atenciosamente,</p>
            <p>Equipe da InkDash</p>
        """
        
        message = MessageSchema(
            subject="Lembrete de Tatuagem Marcada - InkDash",
            recipients=[emailusuario],
            body=html,
            subtype=MessageType.html
        )
        
        # Envio do e-mail
        await fm.send_message(message)
    except Exception as e:
        # Tratamento de exceções
        print("Erro ao enviar e-mail:", e)

