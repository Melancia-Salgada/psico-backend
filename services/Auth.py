import hashlib
from configs.db import create_mongodb_connection
from services.Exceptions import Exceptions

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "easypsi"
collection_name = "psicologo"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] 

class Authenticator:
    def __init__(self):
       pass

    def authenticate_user(self,username:str, password:str): # autenticar e retornar um usuário
        try:
            user = self.get_user(username, password)
            if not user:
                raise Exceptions.user_senha_incorretos()
            print("Achou o usuário")

            senha_armazenada = user["password"]        
            if self.verificar_senha_encriptada(senha_armazenada,password):
                return user
            
        except Exception:
            raise Exceptions.user_senha_incorretos()
        

    # esta função pesquisa um usuário no banco por username e password (encriptado)
    def get_user (self,username: str, password:str):
        senha_criptografada = hashlib.sha256(password.encode()).hexdigest()
    
        # Impressões para debug
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Senha Criptografada: {senha_criptografada}")
        
        # Buscar o usuário
        user = collection.find_one({"username": username, "password": senha_criptografada})
        
        print(f"Usuário encontrado: {user}")
        
        if user:
            user['_id'] = str(user['_id'])  # Convertendo o ObjectId para string
            return user
        else:
            print("Usuário não localizado")
        return False
        
    @staticmethod
    def verificar_senha_encriptada(senha_armazenada:str,password:str) -> bool:
        print(senha_armazenada)
        senha_criptografada = hashlib.sha256(password.encode()).hexdigest()
        print(senha_criptografada)

        if senha_armazenada == senha_criptografada:
            return True
        return False
        
        
    
   
