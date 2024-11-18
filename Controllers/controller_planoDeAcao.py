from configs.db import create_mongodb_connection
from services.Exceptions import Exceptions
from fastapi import status
from models.planoDeAcaoModel import PlanoDeAcao

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "easypsi"
collection_name = "planos_de_acao"


# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] 

class ControllerPlanoDeAcao:
    
    @staticmethod
    def insertPlanoDeAcao(planoDeAcao : PlanoDeAcao):
        try:
            planoDict = dict(planoDeAcao)
            collection.insert_one(planoDict)
        except Exception:
            Exceptions.erro_manipular_usuario()
    
    @staticmethod
    #plano de ação
    def getPlanosDeAcao(email : str):
        try:
        # Debugging the raw cursor output
            planos = collection.find({"email" : email}, {"texto": 1, "_id": 0})
            planosList = list(planos) 
            
            
            return {"planos" : planosList}
        except Exception:
            Exceptions.erro_manipular_usuario()