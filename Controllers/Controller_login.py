from Controllers.token import Token
from services.Auth import Authenticator # importa o autenticador de usuário
from datetime import datetime, timedelta, timezone
from Controllers.token import ACCESS_TOKEN_EXPIRE_MINUTES,Token
from fastapi import HTTPException, status
from services.Exceptions import Exceptions
from models.userModel import usuario_admin_json


class LoginController:
    def __init__(self):
        pass
    
    def login(self, username: str, password: str) -> str:
        try:
            jwt_token = Token()  
            auth = Authenticator()

            #if username ==  usuario-usuario_admin_json["username"] and password ==  usuario-usuario_admin_json["password"]:
                #access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
                #token = jwt_token.create_access_token({"sub": usuario-usuario_admin_json["tipo"], "email":usuario["email"]}, access_token_expires) 
                #return token
        
            usuario = auth.authenticate_user(username,password)
            if usuario:
                access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
                token = jwt_token.create_access_token({"sub":usuario["tipo"], "email":usuario["email"]}, access_token_expires) 
                return token
            
            
        
            else:
                raise Exceptions.user_senha_incorretos()
        except Exception:
            raise Exceptions.user_senha_incorretos()

    def retornar_token_admin( token: str | None = None):
        try:
            jwt_token = Token() 
            jwt = jwt_token.verificar_token(token) 
            tipo =  jwt["sub"]
            if tipo=="Administrador":
                print(tipo)
                return jwt
            else:
                raise Exceptions.acesso_restrito_adm()
        except Exception:
            raise Exceptions.acesso_restrito_adm()
        
    def retornar_token(Authorization:str):
        jwt_token  = Token()
        token = jwt_token.verificar_token(Authorization)
        if not token:
            raise Exceptions.token_invalido()
        return token
  
      
    def tipo_token(token:str):
        print(token)
        try:
            jwt_token = Token()
            token = jwt_token.verificar_token(token)
            print(token)
            tipo =  token["sub"]
            if tipo=="Administrador" or tipo =="Tatuador":
                print(tipo)
                return tipo    
            else:
                raise Exceptions.token_invalido()     
        except Exception:
            raise Exceptions.acesso_restrito_adm()
    
    

