from configs.db import create_mongodb_connection
from models.userModel import Paciente
from services.Exceptions import Exceptions
from fastapi import status


# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "easypsi"
collection_name = "pacientes"


# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] 

class ControllerPaciente:

    @staticmethod
    def buscarPaciente(nomeCompleto : str):
        try:
            paciente = collection.find_one({"nomeCompleto" : nomeCompleto})
            paciente["_id"] = str(paciente["_id"])
            return paciente
        except Exception:
            raise Exceptions.erro_manipular_cliente

    @staticmethod
    def desativarPaciente(paciente : Paciente): 
      try:
        collection.update_one({"nomeCompleto" : paciente.nomeCompleto}, {"$set" : {"status" : "Inativo"}})  
        return {"Sucesso: " : "Paciente desativado"}
      except Exception: 
        raise Exceptions.erro_manipular_cliente()

            
    @staticmethod
    def updatePaciente(user_data: dict, nomeCompleto:str): 
        try:
            print(user_data)
            query = {"nomeCompleto": nomeCompleto}
            print(query)
            campos = [
                        "nomeCompleto",
                        "sexo",
                        "idade",
                        "telefone",
                        "email",
                        "grupo",
                        "nomeCompletoResponsavel",
                        "telefoneResponsavel",
                        "tipo"
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

    #FAZER UMA LIST DENTRO DE CASA PSICOLOGO E INSERIR O PACIENTE LÁ SERIA MT MELHOR
    async def insertPacienteTest(paciente : Paciente) -> dict:
      collection.insert_one(dict(paciente))
      return {"SE DER '201' TÁ QUERENDO: " : status.HTTP_201_CREATED}


    @staticmethod
    def getAllPacientes():
      try: 
        pacientes = [pc for pc in collection.find({"tipo" : "Paciente"})]
        
        for pc in pacientes:
          pc["_id"] = str(pc["_id"])
        
        return {"Pacientes" : pacientes}
      except Exception:
        raise Exceptions.erro_manipular_cliente
    
    


