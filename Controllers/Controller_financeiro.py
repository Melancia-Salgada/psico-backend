from configs.db import create_mongodb_connection
from models.pacienteModel import Paciente
from services.Exceptions import Exceptions
from services.pdf_html import Recibo
from Controllers.Controller_user import ControllerUser
from Controllers.controller_paciente import ControllerPaciente
from fastapi import status
import datetime




connection_string = "mongodb://localhost:27017/"
database_name = "easypsi"
collection_name = "financeiro"


# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] 


class Controller_Recibo:
    def __init__(self) -> None:
        pass

    
    def emitirRecibo(email_paciente:str,psicologo:dict) :

        try:
            emailPsi = psicologo["email"]
            psi = ControllerUser.getSingleUser(emailPsi)

            paciente = ControllerPaciente.buscarPaciente(email_paciente)
            nome_paciente = paciente["nomeCompleto"]
            cpf_paciente = paciente["cpf"]
            valor_paciente = paciente["valor"]

            data = Controller_Recibo.extrairDataAtual()

            nome_psi = psi["username"]
            cpf_psi = psi["CPF"]
            #print(psi)
            r = Recibo()
            r.gerarRecibo(nome_psi,cpf_psi,data, nome_paciente, cpf_paciente, valor_paciente)

        except Exception as ex:
             return(f"Erro: {ex}")
        

    @staticmethod
    def extrairDataAtual():

        data_atual = datetime.datetime.now()
        data_formatada = data_atual.strftime("%d/%m/%Y")
        return data_formatada
