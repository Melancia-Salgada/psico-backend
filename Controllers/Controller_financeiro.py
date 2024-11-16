from configs.db import create_mongodb_connection
#from models.dadosClinicosModel import dadosClinicos
from models.pacienteModel import Paciente
from services.Exceptions import Exceptions
from fastapi import status

connection_string = "mongodb://localhost:27017/"
database_name = "easypsi"
collection_name = "financeiro"


# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] 


class Controller_Recibo:
    def __init__(self) -> None:
        pass

    def emitirRecibo() -> None:
        return True