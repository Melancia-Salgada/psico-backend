from configs.db import create_mongodb_connection
#from models.dadosClinicosModel import dadosClinicos
from models.pacienteModel import Paciente, dadosClinicos
from services.Exceptions import Exceptions
from fastapi import status
from models.planoDeAcaoModel import PlanoDeAcao

# Configurações de conexão com o MongoDB
connection_string = "mongodb://localhost:27017/"
database_name = "easypsi"
collection_name = "pacientes"


# Criando uma conexão com o MongoDB
db = create_mongodb_connection(connection_string, database_name)
collection = db[collection_name] 

class ControllerPaciente:

    @staticmethod
    def buscarPaciente(email : str):
        try:
            paciente = collection.find_one({"email" : email})
            paciente["_id"] = str(paciente["_id"])
            return paciente
        except Exception:
            raise Exceptions.erro_manipular_cliente

    @staticmethod
    def desativarPaciente(email : str): 
      try:
        collection.update_one({"email" : email}, {"$set" : {"status" : "Inativo"}})  
        return {"Sucesso: " : "Paciente desativado"}
      except Exception: 
        raise Exceptions.erro_manipular_cliente()
      
    @staticmethod
    def ativarPaciente(email : str): 
      try:
        collection.update_one({"email" : email}, {"$set" : {"status" : "Ativo"}})  
        return {"Sucesso: " : "Paciente ativado"}
      except Exception: 
        raise Exceptions.erro_manipular_cliente()
      
    @staticmethod
    def setPacientePago(emailPaciente : str):
      try:
        paciente = collection.find_one({"email" : emailPaciente})
        #Atualiza o paciente
        collection.update_one({"email" : emailPaciente}, {"$set" : {"mensalPago" : True}})
        return paciente
      except Exception:
        raise Exceptions.erro_manipular_cliente()
        

            
    @staticmethod
    def updatePaciente(user_data: dict, email : str): 
        try:
            print(user_data)
            query = {"email": email}
            print(query)
            campos = [
                        "nomeCompleto",
                        "sexo",
                        "idade",
                        "telefone",
                        "email",
                        "cpf",
                        "grupo",
                        "valor",
                        "nomeCompletoResponsavel",
                        "telefoneResponsavel",
                        "emailPsi",
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

    async def insertPaciente(paciente : Paciente, psicologo : dict):
      try:

        existingUser = collection.find_one({"email":paciente.email})
        if existingUser :
          raise Exceptions.usuario_existente()
        
        paciente.emailPsi = psicologo["email"]
        print("email psicologo chegou aqui")
        collection.insert_one(paciente.dict(by_alias=True))
        print("chegou aqui")
        return {"Criado" : "Paciente criado com sucesso!"}
      except Exception as ex:
        raise Exceptions.erro_paciente()


    @staticmethod
    def getAllPacientes(psicologo : dict):
      emailPsi = psicologo["email"]
      try: 
        pacientes = [pc for pc in collection.find({"$and":[{"tipo" : "Paciente"}, {"emailPsi" : emailPsi}]})]
        
        for pc in pacientes:
          pc["_id"] = str(pc["_id"])
        
        return {"Pacientes" : pacientes}
      except Exception:
        raise Exceptions.erro_manipular_cliente()
            
     #dados clínicos
    @staticmethod
    def registrar_dado_clinico(email_paciente: str, registro: dadosClinicos):
      try:
          paciente = collection.find_one({"email": email_paciente})

          if not paciente:
              raise Exceptions.erro_manipular_cliente()

          # Inicializar `dados_clinicos` caso esteja vazio
          dados_clinicos = paciente.get("dados_clinicos", [])

          # Converte o objeto de registro para um dicionário e adiciona à lista
          dados_clinicos.append(dict(registro))  # Usa dict() para converter

          # Atualizar a lista `dados_clinicos` no MongoDB
          result = collection.update_one(
              {"email": email_paciente},
              {"$set": {"dados_clinicos": dados_clinicos}}
          )

          if result.modified_count > 0:
              return {"message": "Dado clínico registrado com sucesso"}
          else:
              raise Exceptions.erro_manipular_cliente()
      except Exception as ex:
          print(f"Erro: {ex}")  # Exibir o erro para debugging
          raise Exceptions.erro_manipular_cliente2()
      

    @staticmethod
    def listar_dado_clinico(email_paciente: str):
       try:
          paciente = collection.find_one({"email": email_paciente})

          if not paciente:
              print("Erro: paciente não encontrado.")
              raise Exceptions.erro_manipular_cliente()

          dados_clinicos = paciente.get('dados_clinicos',[])
          return dados_clinicos
          
       except Exception:
          raise Exceptions.erro_manipular_cliente()
        




    
    


