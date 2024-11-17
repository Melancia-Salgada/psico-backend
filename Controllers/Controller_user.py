from configs.db import create_mongodb_connection
from models.userModel import User, Psicologo,Admin
import hashlib
from services.Exceptions import Exceptions
from fastapi import HTTPException,status
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import hashlib

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "easypsi"
collection_name = "usuarios"

collection_nome_paciente = "paciente"

collection_name_codigo = "codigo_login"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] #todas as operações de usuarios podem usar essa collection

collection_codigo = db[collection_name_codigo] #todas as operações de usuarios podem usar essa collection

collection_paciente = db[collection_nome_paciente]

class ControllerUser:
    codigo_login = ""
    def __init__(self) -> None:
     pass

    @staticmethod
    def insertUser(psi:Psicologo)->dict:
      try:
        existingUser = collection.find_one({"username":psi.username})
        if existingUser :
          raise Exceptions.usuario_existente()
  
        senha_criptografada = hashlib.sha256(psi.password.encode()).hexdigest()
        psi.password = senha_criptografada
        print(psi)

        result = collection.insert_one(dict(psi))
        if not result:
          raise ValueError("Erro ao manipular usuário")
        return {"message": status.HTTP_200_OK}
      except HTTPException:
        raise Exceptions.usuario_existente()
      except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Erro ao manipular usuário")
      

    
    @staticmethod
    async def obterCodigoConfirmacao(psi:Psicologo):
      from services.Email import ControllerEmail
      try:
        codigo_confirmacao = await ControllerEmail.enviarEmailConfirmacao(dict(psi))
        ControllerUser.codigo_login = codigo_confirmacao
        result = collection_codigo.insert_one({"codigo":codigo_confirmacao})
        return psi

      except Exception:
         raise Exceptions.erro_email()
       
    #SOMENTE PARA TESTE NAO UTILIZAR EM PRODUCAO
    @staticmethod
    async def insertPsiTest(psi:Psicologo) -> dict:
      collection.insert_one(dict(psi))
      return {"message: " : status.HTTP_201_CREATED}
    

      
    

    @staticmethod 
    async def insertPsi(psi:Psicologo, codigo_digitado:str)->dict: #
      try:
        existingPsi = collection.find_one({"username":psi.username})
        if existingPsi :
          raise Exceptions.usuario_existente()
  
        senha_criptografada = hashlib.sha256(psi.password.encode()).hexdigest()
        psi.password = senha_criptografada
        print(psi)

        
        #codigo_confirmacao = await ControllerEmail.enviarEmailConfirmacao(dict(psi))
        busca_codigo  = collection_codigo.find_one({"codigo":codigo_digitado})
        print(busca_codigo)
        if busca_codigo == None :
             raise ValueError("Código incorreto. Por favor digite novamente")
        
        if busca_codigo :
          result = collection.insert_one(dict(psi))

          deleta_codigo = collection_codigo.find_one_and_delete({"codigo":codigo_digitado})
        
          if not result:
            raise ValueError("Erro ao manipular usuário Psicologo")
          
           # Após inserir no banco, cria a agenda no Google Calendar
          calendar_id = await ControllerUser.create_google_calendar(psi)
                
          # Salva o ID da agenda no banco de dados
          collection.update_one(
              {"_id": result.inserted_id},
              {"$set": {"google_calendar_id": calendar_id}}
          )

        return {"message": status.HTTP_200_OK}
      except HTTPException:
        raise Exceptions.usuario_existente()
      except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
      

    @staticmethod
    async def create_google_calendar(psi: Psicologo):
        """Cria uma nova agenda no Google Calendar para o psicólogo"""
        # Realiza o fluxo OAuth 2.0 para autenticação do Google
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)  # O arquivo JSON deve conter suas credenciais do Google API
        credentials = flow.run_local_server(port=0)  # Abre a autenticação no navegador

        # Constrói o serviço da API Calendar
        service = build('calendar', 'v3', credentials=credentials)

        # Cria a nova agenda
        calendar = {
            'summary': f'Agenda do Psicólogo {psi.username}',
            'timeZone': 'America/Sao_Paulo'
        }

        created_calendar = service.calendars().insert(body=calendar).execute()

        # Retorna o ID da nova agenda criada
        return created_calendar['id']
      

    
    @staticmethod
    def insertUserAdmin(adm:Admin)->dict:
      try:
        existingUser = collection.find_one({"username":adm.username})
        if existingUser :
          raise Exceptions.usuario_existente()
  
        senha_criptografada = hashlib.sha256(adm.password.encode()).hexdigest()
        adm.password = senha_criptografada
        print(adm)

        result = collection.insert_one(dict(adm))
        if not result:
          raise ValueError("Erro ao manipular usuário")
        return {"message": status.HTTP_200_OK}
      except HTTPException:
        raise Exceptions.usuario_existente()
      except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Erro ao manipular usuário")

      
    @staticmethod
    def getAllUsers():
        try:
      # Obtendo todos os documentos da coleção como uma lista de dicionários
          users = [psi for psi in collection.find({})]  # pega cada elemento da collection e armazena na lista

        # Convertendo o campo '_id' para uma string em cada documento, é necessário para retornar 
          for psi in users:
            psi["_id"] = str(psi["_id"])

          return {"users": users}
        except Exception:
         raise Exceptions.erro_manipular_usuario()
        
    @staticmethod
    def getAllUsersPendentes():
        try:
      # Obtendo todos os documentos da coleção como uma lista de dicionários
          users = [psi for psi in collection.find({"status": {"$exists": True, "$eq": "Pendente"}})]
      # pega cada elemento da collection e armazena na lista

        # Convertendo o campo '_id' para uma string em cada documento, é necessário para retornar 
          for psi in users:
            psi["_id"] = str(psi["_id"])

          return {"users": users}
        except Exception:
         raise Exceptions.erro_manipular_usuario()
        
    @staticmethod
    def aprovarPsi(CPF : str):
      collection.update_one({"CPF" : CPF}, {"$set" : {"status" : "aprovado"}})

    @staticmethod
    def desaprovarPsi(CPF : str):
      collection.update_one({"CPF" : CPF}, {"$set" : {"status" : "cancelado"}})
            

    @staticmethod
    def getUser(username):
        try:
            users = collection.find({"username": username})
            print(users)
            if not users:
               raise Exceptions.erro_manipular_usuario()
            
            found_users = []
            for psi in users:
                # Convert ObjectId to string if needed
                psi["_id"] = str(psi["_id"])
                found_users.append(psi)
            return found_users
        except Exception:
         raise Exceptions.erro_manipular_usuario()

    @staticmethod
    def getSingleUser(email):
        try:
            psi = collection.find_one({"email": email})
            return psi
        except Exception:
          raise Exceptions.erro_manipular_usuario()

    @staticmethod
    def editUser(email):
      try:
        psi  = collection.find({"email":email})
        return psi
      except Exception:
        raise Exceptions.erro_manipular_usuario()
      
    @staticmethod
    def updateUser(user_data: dict, username:str): 
        try:
            print(user_data)
            query = {"username": username}
            print(query)
            campos = [
                        "username",
                        "password",
                        "phonenumber",
                        "email",
                        "CRP",
                        "CPF",
                        "tipo",
                        "status"
                      ]

            camposAtualizados = {}
            for campo in campos:
                if campo in user_data and (user_data[campo] is not None and user_data[campo] != ""):
                    camposAtualizados[campo] = user_data[campo]

            new_values = {"$set": camposAtualizados}
            print(new_values)
            result = collection.update_one(query, new_values)
            print(result)

            if result.modified_count > 0:
                return {"message": "Usuário atualizado com sucesso"}
            else:
                raise Exceptions.erro_manipular_usuario()
        except Exception:
            raise Exceptions.erro_manipular_usuario()
    
            
    @staticmethod
    def update_user_senha(user_data):
      try:
          query = {"email": str(user_data["email"])}
          new_password = str(user_data["password"])
          senha_criptografada = hashlib.sha256(new_password.encode()).hexdigest()
          new_values = {"$set": {"password":senha_criptografada}}
          result = collection.update_one(query, new_values)


          if result.modified_count > 0:
              return {"message": "Senha do usuário atualizada com sucesso"}
          else:
              raise Exceptions.erro_manipular_usuario()
      except Exception as e:
          print(f"Erro ao atualizar a senha do usuário: {str(e)}")
          raise HTTPException(status_code=500, detail="Erro interno ao atualizar a senha do usuário")

    @staticmethod
    def deleteUser(username):
      try:
        query  = {"username":username}
        if not query:
           raise Exceptions.erro_manipular_usuario()
        result = collection.delete_one(query)
        if result:
            return {"message": "Usuário deletado com sucesso"}
        else:
            raise Exceptions.erro_manipular_usuario()
      except Exception:
        raise Exceptions.erro_manipular_usuario()
      

    def retornar_psicologo(self,psicologo_logado: dict):
        psi = self.getSingleUser(psicologo_logado["email"])
        return psi["google_calendar_id"]
      
