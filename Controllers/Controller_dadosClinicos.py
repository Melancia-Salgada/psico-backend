from fastapi import HTTPException, status
from models.dadosClinicosModel import dadosClinicos
from configs.db import create_mongodb_connection
from pydantic import ValidationError
from typing import Dict, Any
from services.Exceptions import Exceptions
import hashlib

# Configuração de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "easypsi"
collection_nome_dadosClinicos = "dadosClinicos"

db = create_mongodb_connection(connection_string, database_name)
collection_dadosClinicos = db[collection_nome_dadosClinicos]

class ControllerDadosClinicos:
    def __init__(self) -> None:
     pass

    @staticmethod 
    def insertDadosClinicos(dc:dadosClinicos)->dict:
      try:
        existingUser = collection_dadosClinicos.find_one({"nomeCompleto":dc.nomeCompleto})
        if existingUser :
          raise Exceptions.usuario_existente()
  
        senha_criptografada = hashlib.sha256(dc.password.encode()).hexdigest()
        dc.password = senha_criptografada
        print(dc)

        result = collection_dadosClinicos.insert_one(dict(dc))
        if not result:
          raise ValueError("Erro ao manipular usuário")
        return {"message": status.HTTP_200_OK}
      except HTTPException:
        raise Exceptions.usuario_existente()
      except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Erro ao manipular usuário")
      

    @staticmethod
    def buscarDadosClinicos(email: str):
        try:
            # Busca o registro no MongoDB pelo email
            dados_clinicos = collection_dadosClinicos.find_one({"email": email})

            if not dados_clinicos:
                raise Exceptions.erro_usuario_nao_encontrado()  # Exceção personalizada

            # Converte o _id para string para evitar problemas de serialização
            dados_clinicos["_id"] = str(dados_clinicos["_id"])
            return dados_clinicos

        except Exception as e:
            # Logando o erro para ajudar na depuração
            print(f"Erro ao buscar dados clínicos: {str(e)}")
            raise Exceptions.erro_manipular_usuario()  # Exceção personalizada
    

    
