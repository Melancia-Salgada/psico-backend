from configs.db import create_mongodb_connection
from models.userModel import User, Psicologo,Admin
import hashlib
from services.Exceptions import Exceptions
from fastapi import HTTPException,status
import logging

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "easypsi"
collection_name = "usuarios"

# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] #todas as operações de usuarios podem usar essa collection

class ControllerUser:
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
          users = [psi for psi in collection.find({"status": {"$exists": True, "$eq": "pendente"}})]
  # pega cada elemento da collection e armazena na lista

        # Convertendo o campo '_id' para uma string em cada documento, é necessário para retornar 
          for psi in users:
            psi["_id"] = str(psi["_id"])

          return {"users": users}
        except Exception:
         raise Exceptions.erro_manipular_usuario()

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
                        "pokename",
                        "pokeid",
                        "poketype",
                        "cep",
                        "logradouro",
                        "bairro",
                        "estado"
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

    @staticmethod 
    def insertPsi(psi:Psicologo)->dict:
      try:
        existingPsi = collection.find_one({"username":psi.username})
        if existingPsi :
          raise Exceptions.Psicologo_existente()
  
        senha_criptografada = hashlib.sha256(psi.password.encode()).hexdigest()
        psi.password = senha_criptografada
        print(psi)

        result = collection.insert_one(dict(psi))
        if not result:
          raise ValueError("Erro ao manipular usuário Psicologo")
        return {"message": status.HTTP_200_OK}
      except HTTPException:
        raise Exceptions.Psicologo_existente()
      except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Erro ao manipular usuário")